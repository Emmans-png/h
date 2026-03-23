from django.contrib import admin
from .models import CalorieLog, UserProfile, WeightLog

# Register your models here.
@admin.register(CalorieLog)
class CalorieLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_name', 'calories', 'category', 'date')
    list_filter = ('category', 'date', 'user')
    search_fields = ('food_name', 'user__username')
    readonly_fields = ('date',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'height', 'current_weight', 'target_weight', 'goal', 'bmr')
    list_filter = ('gender', 'goal')
    search_fields = ('user__username',)
    readonly_fields = ('bmr',)

@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'date', 'notes')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'notes')
    readonly_fields = ('date',)