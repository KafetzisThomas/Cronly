from django import forms

from .models import CronJob


class CronJobForm(forms.ModelForm):
    class Meta:
        model = CronJob
        fields = ["target"]
        widgets = {
            "target": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter target"})
        }
