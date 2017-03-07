from django import forms
from models import *

class StreamFilterInputForm(forms.Form):
    Keywords = forms.CharField(required = True,widget=forms.Textarea)
    Location = forms.CharField(required = True)
    class Meta:
        fields = ('Keywords', 'Location')