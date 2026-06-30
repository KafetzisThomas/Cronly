from django.db import models
from django.conf import settings


class Monitor(models.Model):
    target = models.URLField()
    interval_seconds = models.IntegerField(default=300)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.target
