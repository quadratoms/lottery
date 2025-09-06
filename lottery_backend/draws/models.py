from django.db import models

class Draw(models.Model):
    class DrawStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CLOSED = 'CLOSED', 'Closed'
        RESULTED = 'RESULTED', 'Resulted'

    game = models.ForeignKey('games.GameConfig', on_delete=models.PROTECT)
    scheduled_at = models.DateTimeField(db_index=True)
    locked_at = models.DateTimeField()
    status = models.CharField(max_length=16, choices=DrawStatus.choices, default=DrawStatus.PENDING)
    seed_commit_hash = models.CharField(max_length=64)
    seed_reveal = models.CharField(max_length=128, null=True, blank=True)
    winning_number = models.PositiveSmallIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-scheduled_at']


    def __str__(self):
        return f"Draw for {self.game.name} at {self.scheduled_at}"