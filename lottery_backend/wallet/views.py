from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet, LedgerEntry
from .serializers import WalletSerializer, LedgerEntrySerializer
from accounts.permissions import IsPlayer

class WalletDetailView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated, IsPlayer]

    def get_object(self):
        return self.request.user.wallet

class LedgerEntryListView(generics.ListAPIView):
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsPlayer]

    def get_queryset(self):
        return self.queryset.filter(wallet__user=self.request.user).order_by('-created_at')
