from django.db import models
from django.conf import settings

class Ticket(models.Model):
    class TicketStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        WON = 'WON', 'Won'
        LOST = 'LOST', 'Lost'
        VOID = 'VOID', 'Void'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    draw = models.ForeignKey('draws.Draw', on_delete=models.PROTECT)
    selection = models.PositiveSmallIntegerField()  # 1..99
    stake = models.DecimalField(max_digits=12, decimal_places=2)
    potential_payout = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=16, choices=TicketStatus.choices, default=TicketStatus.PENDING)
    placed_at = models.DateTimeField(auto_now_add=True)
    ticket_hash = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return f"Ticket {self.id} for {self.user.username}"