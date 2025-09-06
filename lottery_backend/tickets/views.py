from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from rest_framework import viewsets
from .serializers import TicketCreateSerializer, TicketSerializer
from .models import Ticket
from wallet.models import Wallet, LedgerEntry
from games.models import GameConfig, OddsScheme
from draws.models import Draw
from accounts.permissions import IsPlayer
import hashlib
from django.utils import timezone

class TicketPlaceView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPlayer]

    def post(self, request):
        serializer = TicketCreateSerializer(data=request.data)
        if serializer.is_valid():
            game_id = serializer.validated_data['game_id']
            draw_id = serializer.validated_data['draw_id']
            selection = serializer.validated_data['selection']
            stake = serializer.validated_data['stake']

            w = Wallet.objects.get_or_create(user=request.user, defaults={'currency': 'NGN', 'available': 100000, 'locked': 0})
            with transaction.atomic():
                try:
                    wallet = Wallet.objects.select_for_update().get(user=request.user)
                except Wallet.DoesNotExist:
                    return Response({'detail': 'Wallet not found.'}, status=status.HTTP_404_NOT_FOUND)

                if wallet.available < stake:
                    return Response({'detail': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    game_config = GameConfig.objects.get(id=game_id)
                    draw = Draw.objects.get(id=draw_id, game=game_config)
                except (GameConfig.DoesNotExist, Draw.DoesNotExist):
                    return Response({'detail': 'Game or Draw not found.'}, status=status.HTTP_404_NOT_FOUND)

                if draw.status != Draw.DrawStatus.PENDING:
                    return Response({'detail': 'Draw is not open for betting.'}, status=status.HTTP_400_BAD_REQUEST)

                # Check if current time is past locked_at
                if timezone.now() > draw.locked_at:
                    return Response({'detail': 'Wagering for this draw is closed.'}, status=status.HTTP_400_BAD_REQUEST)

                wallet.available -= stake
                wallet.locked += stake
                wallet.save()

                # Calculate potential payout based on OddsScheme
                odds_scheme = game_config.odds_scheme
                potential_payout = stake * odds_scheme.payout_multiplier

                # Generate ticket hash
                ticket_data = f"{request.user.id}-{draw.id}-{selection}-{stake}-{timezone.now()}"
                ticket_hash = hashlib.sha256(ticket_data.encode()).hexdigest()

                ticket = Ticket.objects.create(
                    user=request.user,
                    draw=draw,
                    selection=selection,
                    stake=stake,
                    potential_payout=potential_payout,
                    ticket_hash=ticket_hash
                )

                LedgerEntry.objects.create(
                    wallet=wallet,
                    type='BET_PLACE',
                    amount=stake,
                    balance_after=wallet.available,
                    ref=f'ticket_{ticket.id}',
                    meta={'ticket_id': ticket.id}
                )

                return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsPlayer]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
