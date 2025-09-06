from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.permissions import IsOpsAdmin

class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOpsAdmin]

    def get(self, request):
        return Response({'message': 'Welcome to the Admin Dashboard!'}, status=status.HTTP_200_OK)
