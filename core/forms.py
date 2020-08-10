from django import forms
import datetime

class TMCForm(forms.Form):
    hoy = datetime.datetime.now()
    limite =  datetime.datetime(hoy.year, hoy.month, 14)    
    montoUF=forms.DecimalField(label="montoUF", required=True, decimal_places=2, min_value=1, localize=True, max_digits = 8, widget=forms.NumberInput(
        attrs={'class':'input--style-5'}
    ),initial=0)
    plazo=forms.IntegerField(label="plazo", required=True, min_value=1, widget=forms.NumberInput(
        attrs={'class':'input--style-5'}
    ),initial=0)
    fechaSolicitud=forms.DateField(label="fechaSolicitud",  required=True, widget=forms.DateInput(
        format = ('%d-%m-%Y'),
        attrs={'class':'input--style-5', 'type':'date', 'max':limite.strftime("%Y-%m-%d")}
    ) , initial=hoy.strftime("%Y-%m-%d"))