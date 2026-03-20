from django import forms
from .models import CalorieLog

class CalorieForm(forms.ModelForm):
    class Meta:
        model = CalorieLog
        fields = ['food_name', 'calories', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'})
        }
