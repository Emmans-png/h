from django import forms
from .models import CalorieLog, UserProfile, WeightLog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

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
        # Add custom password help text
        self.fields['password1'].help_text = (
            "Password must be at least 8 characters long."
        )
        self.fields['password2'].help_text = (
            "Enter the same password as above, for verification."
        )
        
        # Add placeholder attributes
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        return username

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'height', 'current_weight', 'target_weight', 'goal']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '120'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '50', 'max': '300'}),
            'current_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '20', 'max': '500'}),
            'target_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '20', 'max': '500'}),
            'goal': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 1 or age > 120:
            raise forms.ValidationError("Please enter a valid age between 1 and 120.")
        return age
    
    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height < 50 or height > 300:
            raise forms.ValidationError("Please enter a valid height between 50 and 300 cm.")
        return height
    
    def clean_current_weight(self):
        weight = self.cleaned_data.get('current_weight')
        if weight < 20 or weight > 500:
            raise forms.ValidationError("Please enter a valid weight between 20 and 500 kg.")
        return weight
    
    def clean_target_weight(self):
        weight = self.cleaned_data.get('target_weight')
        if weight < 20 or weight > 500:
            raise forms.ValidationError("Please enter a valid target weight between 20 and 500 kg.")
        return weight
    
    def clean(self):
        cleaned_data = super().clean()
        current_weight = cleaned_data.get('current_weight')
        target_weight = cleaned_data.get('target_weight')
        goal = cleaned_data.get('goal')
        
        if current_weight and target_weight:
            if goal == 'weight_loss' and target_weight >= current_weight:
                raise forms.ValidationError("For weight loss, target weight should be less than current weight.")
            elif goal == 'weight_gain' and target_weight <= current_weight:
                raise forms.ValidationError("For weight gain, target weight should be greater than current weight.")
            elif goal == 'maintenance' and abs(target_weight - current_weight) > 5:
                raise forms.ValidationError("For maintenance, target weight should be close to current weight (within 5kg).")
        
        return cleaned_data

class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['weight', 'notes']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '20', 'max': '500'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes about this weight entry...'}),
        }
    
    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight < 20 or weight > 500:
            raise forms.ValidationError("Please enter a valid weight between 20 and 500 kg.")
        return weight
