from django import forms
from .models import Predictions


class PredictionForm(forms.ModelForm):
    class Meta:
        model = Predictions
        fields = ["ticker"]