from django.urls import path
from .views import KycInitiateView, KycStatusView

urlpatterns = [
    path('initiate/', KycInitiateView.as_view(), name='kyc_initiate'),
    path('status/', KycStatusView.as_view(), name='kyc_status'),
]
