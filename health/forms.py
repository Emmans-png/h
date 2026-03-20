from django import forms
from .models import CalorieLog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CalorieForm(forms.ModelForm):
    class Meta:
        model = CalorieLog
        fields = ['food_name', 'calories', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'})
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove password validation help text
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        # Remove password validators
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
