from django import forms
from datetime import datetime

class TMCForm(forms.Form):
    montoUF=forms.DecimalField(label="montoUF", required=True, decimal_places=2, localize=True, max_digits = 8, widget=forms.NumberInput(
        attrs={'class':'input--style-5'}
    ),initial=0)
    plazo=forms.IntegerField(label="plazo", required=True, widget=forms.NumberInput(
        attrs={'class':'input--style-5'}
    ),initial=0)
    fechaSolicitud=forms.DateField(label="fechaSolicitud",  required=True, widget=forms.DateInput(
        format = ('%d-%m-%Y'),
        attrs={'class':'input--style-5', 'type':'date'}
    ) , initial=datetime.now().strftime("%Y-%m-%d"))