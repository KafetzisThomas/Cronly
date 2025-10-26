from django import forms

from .models import CronJob

INTERVAL_CHOICES = [
    ("60", "Every minute"),
    ("300", "Every 5 minutes"),
    ("3600", "Hourly"),
    ("86400", "Daily"),
    ("604800", "Weekly"),
    ("2592000", "Monthly"),
    ("custom", "Custom"),
]

class CronJobForm(forms.ModelForm):
    interval_seconds = forms.ChoiceField(
        choices=INTERVAL_CHOICES, widget=forms.Select(attrs={"class": "form-select", "id": "id_interval"})
    )
    custom_interval = forms.IntegerField(
        required=False,
        label="",
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control mt-2",
            "placeholder": "Enter custom interval in seconds",
            "id": "id_custom_interval",
            "style": "display:none;"
        })
    )

    class Meta:
        model = CronJob
        fields = ["target", "interval_seconds", "custom_interval"]
        widgets = {
            "target": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter target URL", "autofocus": True})
        }

    def clean(self):
        cleaned_data = super().clean()
        interval = cleaned_data.get("interval_seconds")
        custom = cleaned_data.get("custom_interval")

        if interval == "custom":
            cleaned_data["interval_seconds"] = custom

        return cleaned_data
