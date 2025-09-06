from rest_framework import viewsets, permissions
from .models import Draw
from .serializers import DrawSerializer

class DrawViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Draw.objects.all()
    serializer_class = DrawSerializer
    permission_classes = [permissions.IsAuthenticated]
