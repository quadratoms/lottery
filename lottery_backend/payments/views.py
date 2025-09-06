from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import DepositSerializer, PaymentSerializer
from .models import Payment
from accounts.permissions import IsPlayer
from django.conf import settings
from django.db import transaction
from wallet.models import Wallet, LedgerEntry
import requests
import json
import hmac
import hashlib

class DepositInitiateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPlayer]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            provider = serializer.validated_data['provider']

            if provider.lower() == 'paystack':
                # Create a pending payment record
                payment = Payment.objects.create(
                    user=request.user,
                    type=Payment.PaymentType.DEPOSIT,
                    provider=provider,
                    amount=amount,
                    status=Payment.PaymentStatus.PENDING
                )

                # Interact with Paystack API
                headers = {
                    "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "email": request.user.email,
                    "amount": int(amount * 100), # Paystack expects amount in kobo
                    "callback_url": settings.PAYSTACK_CALLBACK_URL,
                    "metadata": {
                        "payment_id": payment.id,
                        "user_id": request.user.id
                    }
                }
                try:
                    response = requests.post(
                        "https://api.paystack.co/transaction/initialize",
                        headers=headers,
                        json=payload
                    )
                    response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                    paystack_data = response.json()
                    if paystack_data['status']:
                        payment.external_ref = paystack_data['data']['reference']
                        payment.save()
                        return Response({
                            'payment_id': payment.id,
                            'authorization_url': paystack_data['data']['authorization_url']
                        }, status=status.HTTP_201_CREATED)
                    else:
                        return Response({'detail': paystack_data['message']}, status=status.HTTP_400_BAD_REQUEST)
                except requests.exceptions.RequestException as e:
                    return Response({'detail': f"Paystack API error: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'detail': 'Unsupported payment provider.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaystackWebhookView(APIView):
    permission_classes = [permissions.AllowAny] # No authentication needed for webhooks

    def post(self, request):
        # Verify webhook signature
        paystack_signature = request.headers.get('x-paystack-signature')
        if not paystack_signature:
            return Response({'detail': 'No signature header.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get raw body
        # Django's request.body is already bytes
        body = request.body

        # Hash the body with HMAC SHA512 and compare with signature
        hashed = hmac.new(settings.PAYSTACK_SECRET_KEY.encode('utf-8'), body, hashlib.sha512).hexdigest()

        if hashed != paystack_signature:
            return Response({'detail': 'Invalid signature.'}, status=status.HTTP_400_BAD_REQUEST)

        event = json.loads(body.decode('utf-8'))
        event_type = event.get('event')

        if event_type == 'charge.success':
            reference = event['data']['reference']
            amount_kobo = event['data']['amount']
            amount_naira = amount_kobo / 100

            with transaction.atomic():
                try:
                    payment = Payment.objects.get(external_ref=reference, status=Payment.PaymentStatus.PENDING)
                except Payment.DoesNotExist:
                    print(f"Payment with reference {reference} not found or already processed.")
                    return Response(status=status.HTTP_200_OK) # Return 200 even if not found to avoid re-delivery

                if payment.amount != amount_naira:
                    print(f"Amount mismatch for payment {payment.id}. Expected {payment.amount}, got {amount_naira}")
                    payment.status = Payment.PaymentStatus.FAILED
                    payment.save()
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                payment.status = Payment.PaymentStatus.SUCCESS
                payment.save()

                # Credit wallet
                wallet = Wallet.objects.select_for_update().get(user=payment.user)
                wallet.available += payment.amount
                wallet.save()

                # Create ledger entry
                LedgerEntry.objects.create(
                    wallet=wallet,
                    type='DEPOSIT',
                    amount=payment.amount,
                    balance_after=wallet.available,
                    ref=f'payment_{payment.id}',
                    meta={'payment_id': payment.id, 'provider_ref': reference}
                )
                print(f"Payment {payment.id} confirmed and wallet credited.")

        return Response(status=status.HTTP_200_OK)
