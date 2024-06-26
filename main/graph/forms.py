# graph/forms.py
from django import forms

class GraphForm(forms.Form):
    input_string = forms.CharField(label='Input String')
    start_date = forms.DateField(label='Start Date', widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.TextInput(attrs={'type': 'date'}))
