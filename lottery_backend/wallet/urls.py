from django.urls import path
from .views import WalletDetailView, LedgerEntryListView

urlpatterns = [
    path('balance/', WalletDetailView.as_view(), name='wallet_balance'),
    path('statement/', LedgerEntryListView.as_view(), name='wallet_statement'),
]
