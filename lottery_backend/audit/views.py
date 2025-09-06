from rest_framework import viewsets, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer
from accounts.permissions import IsAuditor, IsOpsAdmin

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuditor | IsOpsAdmin]

    def get_queryset(self):
        # Only allow superusers, Ops/Admin or Auditors to view all audit logs
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Ops/Admin').exists() or self.request.user.groups.filter(name='Auditor').exists():
            return self.queryset.all()
        # Otherwise, users can only view their own actions
        return self.queryset.filter(actor=self.request.user)
