from django import forms
from .models import CommonModel, UserModel

class PythonCodeFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = PythonCodeWidget
        super().__init__(*args, **kwargs)

class PythonCodeWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({
            'class': 'python-code-widget',
            'rows': 20,
            'cols': 80,
        })
        super().__init__(*args, **kwargs)

class StrategyForm(forms.ModelForm):
    ticker = forms.CharField()
    start_date = forms.DateField()
    end_date = forms.DateField()
    stop_loss = forms.DecimalField(max_digits=10, decimal_places=2)
    strategy = forms.CharField()
    class Meta:
        model = CommonModel
        fields = ['ticker', 'start_date', 'end_date', 'stop_loss', 'strategy']

class csvForm(forms.ModelForm):
    csv_file = forms.FileField()
    stop_loss = forms.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = CommonModel
        fields = ['csv_file', 'stop_loss']

class userstrategy(forms.ModelForm):
    strategy = forms.CharField()
    source = PythonCodeFormField(required=False)

    class Meta:
        model = UserModel
        fields = ['strategy', 'source']


