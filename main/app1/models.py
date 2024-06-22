from django import forms
from django.db import models

class PythonCodeField(models.TextField):
    description = "Field to store Python code"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': PythonCodeFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        return errors

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

# class CommonModel(models.Model):
#     name = models.CharField(max_length=100)
#     source = PythonCodeField(blank=True, null=True)
#     def __str__(self):
#         return self.name
class CommonModel(models.Model):
    name = models.CharField(max_length=100)
    source = PythonCodeField(blank=True, null=True)
    def __str__(self):
        return self.name
class UserModel(models.Model):
    owner=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    source=PythonCodeField(blank=True, null=True)

