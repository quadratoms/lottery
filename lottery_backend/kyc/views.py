from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import KycInitiateSerializer, KycCheckSerializer
from .models import KycCheck
from accounts.permissions import IsPlayer, IsOpsAdmin

class KycInitiateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPlayer]

    def post(self, request):
        serializer = KycInitiateSerializer(data=request.data)
        if serializer.is_valid():
            bvn_nin = serializer.validated_data['bvn_nin']

            # In a real scenario, you would interact with a KYC provider API here
            # and get a result. For now, we'll simulate a successful check.
            result = "SUCCESS"
            reference = f"kyc_ref_{request.user.id}_{bvn_nin}"

            kyc_check = KycCheck.objects.create(
                user=request.user,
                provider="SimulatedKYC",
                result=result,
                reference=reference
            )
            return Response(KycCheckSerializer(kyc_check).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KycStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPlayer | IsOpsAdmin]

    def get(self, request):
        kyc_checks = KycCheck.objects.filter(user=request.user).order_by('-created_at')
        if kyc_checks.exists():
            return Response(KycCheckSerializer(kyc_checks.first()).data, status=status.HTTP_200_OK)
        return Response({'detail': 'No KYC checks found.'}, status=status.HTTP_404_NOT_FOUND)
