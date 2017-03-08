from django import forms
from models import *

class StreamFilterInputForm(forms.Form):
    Keywords = forms.CharField(required = True,widget=forms.Textarea(attrs={'rows':4}))
    Location = forms.CharField(required = True)
    Latitude = forms.CharField(required = True)
    Longitude = forms.CharField(required = True)
    class Meta:
        fields = ('Keywords', 'Location','Latitude','Longitude')