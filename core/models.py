from django.contrib.auth.models import User
from django.db import models


class CronJob(models.Model):
    target = models.CharField(max_length=100)
    avg_rtt_ms = models.FloatField()
    min_rtt_ms = models.FloatField()
    max_rtt_ms = models.FloatField()
    interval_seconds = models.IntegerField(default=300)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.target
