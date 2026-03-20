import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracker.settings')

# Setup Django
django.setup()

from health.models import CalorieLog

def categorize_food(food_name):
    """Automatically categorize food based on name"""
    food_name_lower = food_name.lower()
    
    # Proteins
    protein_keywords = ['beef', 'lobster', 'fish', 'eggs', 'chicken', 'turkey', 'pork', 'lamb', 'meat', 'salmon', 'tuna', 'shrimp', 'bacon', 'sausage', 'steak']
    if any(keyword in food_name_lower for keyword in protein_keywords):
        return 'proteins'
    
    # Carbohydrates
    carb_keywords = ['maize', 'seed', 'rice', 'bread', 'pasta', 'potato', 'corn', 'wheat', 'oats', 'quinoa', 'cereal', 'flour', 'sugar']
    if any(keyword in food_name_lower for keyword in carb_keywords):
        return 'carbohydrates'
    
    # Vitamins (fruits and vegetables)
    vitamin_keywords = ['apple', 'banana', 'orange', 'grape', 'berry', 'vegetable', 'salad', 'carrot', 'broccoli', 'spinach', 'tomato', 'onion', 'garlic', 'pepper', 'cucumber', 'lettuce']
    if any(keyword in food_name_lower for keyword in vitamin_keywords):
        return 'vitamins'
    
    # Default to carbohydrates if no match
    return 'carbohydrates'

def update_existing_logs():
    """Update existing CalorieLog entries with proper categories"""
    logs = CalorieLog.objects.all()
    updated_count = 0
    
    for log in logs:
        new_category = categorize_food(log.food_name)
        if log.category != new_category:
            print(f"Updating '{log.food_name}' from '{log.category}' to '{new_category}'")
            log.category = new_category
            log.save()
            updated_count += 1
    
    print(f"\nUpdated {updated_count} food entries with proper categories")

if __name__ == '__main__':
    update_existing_logs()
