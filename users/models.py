from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    discord_webhook_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username
