from django.urls import path
from .views import DepositInitiateView, PaystackWebhookView

urlpatterns = [
    path('deposit/', DepositInitiateView.as_view(), name='deposit_initiate'),
    path('webhook/paystack/', PaystackWebhookView.as_view(), name='paystack_webhook'),
]
