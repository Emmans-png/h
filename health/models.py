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

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('weight_gain', 'Weight Gain'),
        ('maintenance', 'Maintenance'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    current_weight = models.FloatField(help_text="Weight in kg")
    target_weight = models.FloatField(help_text="Target weight in kg")
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    bmr = models.IntegerField(help_text="Basal Metabolic Rate in calories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_bmr(self):
        """Calculate BMR using Mifflin-St Jeor Equation"""
        if self.gender == 'male':
            bmr = 10 * self.current_weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.current_weight + 6.25 * self.height - 5 * self.age - 161
        self.bmr = int(bmr)
        self.save()
        return self.bmr
    
    def get_weight_difference(self):
        """Calculate difference between current and target weight"""
        return self.current_weight - self.target_weight
    
    def get_weight_progress_message(self):
        """Get motivational message based on weight progress"""
        diff = self.get_weight_difference()
        if self.goal == 'weight_loss':
            if diff > 0:
                return f"You need to lose {abs(diff):.1f} kg more to reach your goal!"
            else:
                return f"Congratulations! You've reached your weight loss goal!"
        elif self.goal == 'weight_gain':
            if diff < 0:
                return f"You need to gain {abs(diff):.1f} kg more to reach your goal!"
            else:
                return f"Congratulations! You've reached your weight gain goal!"
        else:
            return "You're maintaining your current weight well!"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField(help_text="Weight in kg")
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Optional notes about this weight entry")
    
    class Meta:
        ordering = ['-date', '-id']
    
    def __str__(self):
        return f"{self.user.username} - {self.weight} kg on {self.date}"
