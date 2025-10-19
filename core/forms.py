from django import forms

from .models import CronJob


class CronJobForm(forms.ModelForm):
    class Meta:
        model = CronJob
        fields = ["target", "interval_seconds"]
        widgets = {
            "target": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Enter target"
            }),
            "interval_seconds": forms.NumberInput(attrs={
                "class": "form-control", "placeholder": "Interval in seconds (e.g. 300)"
            }),
        }
