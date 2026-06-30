from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username']


class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username",)


class DiscordWebhookForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("discord_webhook_url",)
        labels = {
            "discord_webhook_url": "Discord Webhook URL",
        }
        widgets = {
            "discord_webhook_url": forms.URLInput(
                attrs={
                    "placeholder": "https://discord.com/api/webhooks/...",
                }
            )
        }
        help_texts = {
            "discord_webhook_url": (
                "Paste your Discord channel webhook URL here.<br>"
                "Create one in Discord: Server Settings -> Integrations -> Webhooks."
            )
        }
