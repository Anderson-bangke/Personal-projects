from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class GenerateUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )