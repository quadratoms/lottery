from rest_framework import viewsets, generics, permissions
from .models import CustomUser
from .serializers import UserSerializer, RegistrationSerializer
from .permissions import IsOwnerOrOpsAdmin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrOpsAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Ops/Admin').exists():
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
    # authentication_classes = None # Explicitly set no authentication for registration
