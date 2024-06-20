from django import forms
from django.contrib.auth.models import User
from .models import CommonModel

class StrategyForm(forms.ModelForm):
     ticker = forms.CharField()
     start_date = forms.DateField()
     end_date=forms.DateField()
     stop_loss=forms.DecimalField(max_digits=10, decimal_places=2)
     strategy=forms.CharField()
     class Meta:
         model=CommonModel
         fields= ['ticker','start_date','end_date','stop_loss','strategy']