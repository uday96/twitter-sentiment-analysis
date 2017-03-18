from django import forms
from models import *

class StreamFilterInputForm(forms.Form):
    Keywords = forms.CharField(required = True,widget=forms.Textarea(attrs={'rows':4}))
    Location = forms.CharField()
    LatLng = forms.CharField(required = True,widget=forms.HiddenInput())
    class Meta:
        fields = ('Keywords', 'Location','LatLng')