from django.db import models
from django.conf import settings

class KycCheck(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    provider = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KYC Check for {self.user.username}"