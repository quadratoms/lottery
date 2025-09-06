from django.db import models

class Payout(models.Model):
    class PayoutStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'

    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    tax_withheld = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    paid_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=PayoutStatus.choices, default=PayoutStatus.PENDING)

    def __str__(self):
        return f"Payout for Ticket {self.ticket.id}"