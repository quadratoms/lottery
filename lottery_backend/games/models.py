from django.db import models

class GameConfig(models.Model):
    name = models.CharField(max_length=255)
    range_min = models.IntegerField(default=1)
    range_max = models.IntegerField(default=99)
    draw_interval_sec = models.IntegerField()
    lock_offset_sec = models.IntegerField()
    min_bet = models.DecimalField(max_digits=12, decimal_places=2)
    max_bet = models.DecimalField(max_digits=12, decimal_places=2)
    odds_scheme = models.ForeignKey('OddsScheme', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class OddsScheme(models.Model):
    bet_type = models.CharField(max_length=255)
    payout_multiplier = models.DecimalField(max_digits=10, decimal_places=4)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    active_from = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bet_type} - {self.payout_multiplier}x"