# extractor/forms.py
from django import forms
from .models import Estimate

class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = ['pdf_file']
