from rest_framework import viewsets, permissions
from .models import GameConfig, OddsScheme
from .serializers import GameConfigSerializer, OddsSchemeSerializer
from accounts.permissions import IsOpsAdmin

class GameConfigViewSet(viewsets.ModelViewSet):
    queryset = GameConfig.objects.all()
    serializer_class = GameConfigSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsOpsAdmin]
        return super().get_permissions()

class OddsSchemeViewSet(viewsets.ModelViewSet):
    queryset = OddsScheme.objects.all()
    serializer_class = OddsSchemeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsOpsAdmin]
        return super().get_permissions()
