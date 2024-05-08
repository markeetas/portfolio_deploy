from django import forms
from .models import Insured

class InsuredForm(forms.ModelForm):

    class Meta:
        model = Insured
        fields = ["name", "address", "email", "phone"]