from django.urls import path
from .views import NotificationTestView

urlpatterns = [
    path('test/', NotificationTestView.as_view(), name='test_notification'),
]
