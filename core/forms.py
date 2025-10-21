from django import forms

from .models import CronJob

INTERVAL_CHOICES = [
    ("60", "Every minute"),
    ("300", "Every 5 minutes"),
    ("3600", "Hourly"),
    ("86400", "Daily"),
    ("604800", "Weekly"),
    ("2592000", "Monthly"),
]

class CronJobForm(forms.ModelForm):
    interval_seconds = forms.ChoiceField(
        choices=INTERVAL_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = CronJob
        fields = ["target", "interval_seconds"]
        widgets = {
            "target": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter target"})
        }
