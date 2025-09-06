from django.db import models
from django.conf import settings

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    currency = models.CharField(max_length=3, default='NGN')
    available = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    locked = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

class LedgerEntry(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    type = models.CharField(max_length=32)  # BET_PLACE, BET_REFUND, WIN_PAYOUT, DEPOSIT, WITHDRAWAL, FEE
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    balance_after = models.DecimalField(max_digits=14, decimal_places=2)
    ref = models.CharField(max_length=64, db_index=True)
    meta = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} of {self.amount} for {self.wallet.user.username}"