from rest_framework import viewsets, permissions
from .models import Payout
from .serializers import PayoutSerializer
from accounts.permissions import IsPlayer

class PayoutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated, IsPlayer]

    def get_queryset(self):
        return self.queryset.filter(ticket__user=self.request.user)
