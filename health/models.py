from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CalorieLog(models.Model):
    CATEGORY_CHOICES = [
        ('proteins', 'Proteins'),
        ('vitamins', 'Vitamins'),
        ('carbohydrates', 'Carbohydrates'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='carbohydrates')
    date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.food_name} - {self.calories} kcal"
