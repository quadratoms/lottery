from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.permissions import IsOpsAdmin

class NotificationTestView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOpsAdmin]

    def post(self, request):
        message = request.data.get('message', 'Test notification')
        # In a real scenario, you would send an actual notification here
        print(f"Sending test notification: {message}")
        return Response({'status': 'Notification sent'}, status=status.HTTP_200_OK)
