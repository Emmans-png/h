from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CalorieLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.food_name} - {self.calories} kcal"
