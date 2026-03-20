# Comprehensive Food Dictionary with Categories and Calorie Information
# All calorie values are approximate per 100g serving unless otherwise specified

FOOD_DATABASE = {
    # Proteins (Meats, Fish, Eggs, Dairy)
    'beef': {'category': 'proteins', 'calories': 250, 'unit': '100g'},
    'chicken breast': {'category': 'proteins', 'calories': 165, 'unit': '100g'},
    'chicken thigh': {'category': 'proteins', 'calories': 209, 'unit': '100g'},
    'turkey': {'category': 'proteins', 'calories': 189, 'unit': '100g'},
    'pork': {'category': 'proteins', 'calories': 242, 'unit': '100g'},
    'lamb': {'category': 'proteins', 'calories': 294, 'unit': '100g'},
    'bacon': {'category': 'proteins', 'calories': 541, 'unit': '100g'},
    'sausage': {'category': 'proteins', 'calories': 299, 'unit': '100g'},
    'steak': {'category': 'proteins', 'calories': 271, 'unit': '100g'},
    'salmon': {'category': 'proteins', 'calories': 208, 'unit': '100g'},
    'tuna': {'category': 'proteins', 'calories': 144, 'unit': '100g'},
    'cod': {'category': 'proteins', 'calories': 82, 'unit': '100g'},
    'shrimp': {'category': 'proteins', 'calories': 99, 'unit': '100g'},
    'lobster': {'category': 'proteins', 'calories': 89, 'unit': '100g'},
    'eggs': {'category': 'proteins', 'calories': 155, 'unit': '100g'},
    'egg': {'category': 'proteins', 'calories': 155, 'unit': '100g'},
    'milk': {'category': 'proteins', 'calories': 42, 'unit': '100ml'},
    'cheese': {'category': 'proteins', 'calories': 402, 'unit': '100g'},
    'cheddar cheese': {'category': 'proteins', 'calories': 402, 'unit': '100g'},
    'mozzarella': {'category': 'proteins', 'calories': 280, 'unit': '100g'},
    'yogurt': {'category': 'proteins', 'calories': 59, 'unit': '100g'},
    'greek yogurt': {'category': 'proteins', 'calories': 100, 'unit': '100g'},
    'cottage cheese': {'category': 'proteins', 'calories': 98, 'unit': '100g'},
    'butter': {'category': 'proteins', 'calories': 717, 'unit': '100g'},
    'tofu': {'category': 'proteins', 'calories': 76, 'unit': '100g'},
    'tempeh': {'category': 'proteins', 'calories': 193, 'unit': '100g'},
    'beans': {'category': 'proteins', 'calories': 347, 'unit': '100g'},
    'black beans': {'category': 'proteins', 'calories': 132, 'unit': '100g'},
    'kidney beans': {'category': 'proteins', 'calories': 127, 'unit': '100g'},
    'chickpeas': {'category': 'proteins', 'calories': 364, 'unit': '100g'},
    'lentils': {'category': 'proteins', 'calories': 116, 'unit': '100g'},
    'peanuts': {'category': 'proteins', 'calories': 567, 'unit': '100g'},
    'almonds': {'category': 'proteins', 'calories': 579, 'unit': '100g'},
    'walnuts': {'category': 'proteins', 'calories': 654, 'unit': '100g'},
    'cashews': {'category': 'proteins', 'calories': 553, 'unit': '100g'},
    
    # Carbohydrates (Grains, Starches, Sweets)
    'rice': {'category': 'carbohydrates', 'calories': 130, 'unit': '100g'},
    'white rice': {'category': 'carbohydrates', 'calories': 130, 'unit': '100g'},
    'brown rice': {'category': 'carbohydrates', 'calories': 111, 'unit': '100g'},
    'bread': {'category': 'carbohydrates', 'calories': 265, 'unit': '100g'},
    'white bread': {'category': 'carbohydrates', 'calories': 265, 'unit': '100g'},
    'whole wheat bread': {'category': 'carbohydrates', 'calories': 247, 'unit': '100g'},
    'pasta': {'category': 'carbohydrates', 'calories': 131, 'unit': '100g'},
    'spaghetti': {'category': 'carbohydrates', 'calories': 158, 'unit': '100g'},
    'potato': {'category': 'carbohydrates', 'calories': 77, 'unit': '100g'},
    'sweet potato': {'category': 'carbohydrates', 'calories': 86, 'unit': '100g'},
    'corn': {'category': 'carbohydrates', 'calories': 365, 'unit': '100g'},
    'maize': {'category': 'carbohydrates', 'calories': 365, 'unit': '100g'},
    'wheat': {'category': 'carbohydrates', 'calories': 339, 'unit': '100g'},
    'oats': {'category': 'carbohydrates', 'calories': 389, 'unit': '100g'},
    'quinoa': {'category': 'carbohydrates', 'calories': 120, 'unit': '100g'},
    'cereal': {'category': 'carbohydrates', 'calories': 379, 'unit': '100g'},
    'flour': {'category': 'carbohydrates', 'calories': 364, 'unit': '100g'},
    'sugar': {'category': 'carbohydrates', 'calories': 387, 'unit': '100g'},
    'honey': {'category': 'carbohydrates', 'calories': 304, 'unit': '100g'},
    'maple syrup': {'category': 'carbohydrates', 'calories': 260, 'unit': '100g'},
    'chocolate': {'category': 'carbohydrates', 'calories': 546, 'unit': '100g'},
    'dark chocolate': {'category': 'carbohydrates', 'calories': 546, 'unit': '100g'},
    'pizza': {'category': 'carbohydrates', 'calories': 285, 'unit': '100g'},
    'burger': {'category': 'carbohydrates', 'calories': 295, 'unit': '100g'},
    'hamburger': {'category': 'carbohydrates', 'calories': 295, 'unit': '100g'},
    'french fries': {'category': 'carbohydrates', 'calories': 312, 'unit': '100g'},
    'chips': {'category': 'carbohydrates', 'calories': 536, 'unit': '100g'},
    'potato chips': {'category': 'carbohydrates', 'calories': 536, 'unit': '100g'},
    'tortilla': {'category': 'carbohydrates', 'calories': 218, 'unit': '100g'},
    'bagel': {'category': 'carbohydrates', 'calories': 250, 'unit': '100g'},
    'croissant': {'category': 'carbohydrates', 'calories': 406, 'unit': '100g'},
    'pancake': {'category': 'carbohydrates', 'calories': 227, 'unit': '100g'},
    'waffle': {'category': 'carbohydrates', 'calories': 291, 'unit': '100g'},
    'doughnut': {'category': 'carbohydrates', 'calories': 452, 'unit': '100g'},
    'cookie': {'category': 'carbohydrates', 'calories': 502, 'unit': '100g'},
    'cake': {'category': 'carbohydrates', 'calories': 358, 'unit': '100g'},
    'ice cream': {'category': 'carbohydrates', 'calories': 207, 'unit': '100g'},
    
    # Vitamins (Fruits and Vegetables)
    'apple': {'category': 'vitamins', 'calories': 52, 'unit': '100g'},
    'banana': {'category': 'vitamins', 'calories': 89, 'unit': '100g'},
    'orange': {'category': 'vitamins', 'calories': 47, 'unit': '100g'},
    'grape': {'category': 'vitamins', 'calories': 69, 'unit': '100g'},
    'grapes': {'category': 'vitamins', 'calories': 69, 'unit': '100g'},
    'strawberry': {'category': 'vitamins', 'calories': 33, 'unit': '100g'},
    'strawberries': {'category': 'vitamins', 'calories': 33, 'unit': '100g'},
    'blueberry': {'category': 'vitamins', 'calories': 57, 'unit': '100g'},
    'blueberries': {'category': 'vitamins', 'calories': 57, 'unit': '100g'},
    'raspberry': {'category': 'vitamins', 'calories': 52, 'unit': '100g'},
    'raspberries': {'category': 'vitamins', 'calories': 52, 'unit': '100g'},
    'blackberry': {'category': 'vitamins', 'calories': 43, 'unit': '100g'},
    'blackberries': {'category': 'vitamins', 'calories': 43, 'unit': '100g'},
    'mango': {'category': 'vitamins', 'calories': 60, 'unit': '100g'},
    'pineapple': {'category': 'vitamins', 'calories': 50, 'unit': '100g'},
    'watermelon': {'category': 'vitamins', 'calories': 30, 'unit': '100g'},
    'kiwi': {'category': 'vitamins', 'calories': 61, 'unit': '100g'},
    'pear': {'category': 'vitamins', 'calories': 57, 'unit': '100g'},
    'peach': {'category': 'vitamins', 'calories': 39, 'unit': '100g'},
    'plum': {'category': 'vitamins', 'calories': 46, 'unit': '100g'},
    'cherry': {'category': 'vitamins', 'calories': 63, 'unit': '100g'},
    'cherries': {'category': 'vitamins', 'calories': 63, 'unit': '100g'},
    'lemon': {'category': 'vitamins', 'calories': 29, 'unit': '100g'},
    'lime': {'category': 'vitamins', 'calories': 30, 'unit': '100g'},
    'avocado': {'category': 'vitamins', 'calories': 160, 'unit': '100g'},
    'vegetable': {'category': 'vitamins', 'calories': 25, 'unit': '100g'},
    'salad': {'category': 'vitamins', 'calories': 15, 'unit': '100g'},
    'carrot': {'category': 'vitamins', 'calories': 41, 'unit': '100g'},
    'carrots': {'category': 'vitamins', 'calories': 41, 'unit': '100g'},
    'broccoli': {'category': 'vitamins', 'calories': 34, 'unit': '100g'},
    'spinach': {'category': 'vitamins', 'calories': 23, 'unit': '100g'},
    'tomato': {'category': 'vitamins', 'calories': 18, 'unit': '100g'},
    'tomatoes': {'category': 'vitamins', 'calories': 18, 'unit': '100g'},
    'onion': {'category': 'vitamins', 'calories': 40, 'unit': '100g'},
    'onions': {'category': 'vitamins', 'calories': 40, 'unit': '100g'},
    'garlic': {'category': 'vitamins', 'calories': 149, 'unit': '100g'},
    'pepper': {'category': 'vitamins', 'calories': 27, 'unit': '100g'},
    'bell pepper': {'category': 'vitamins', 'calories': 27, 'unit': '100g'},
    'cucumber': {'category': 'vitamins', 'calories': 16, 'unit': '100g'},
    'lettuce': {'category': 'vitamins', 'calories': 15, 'unit': '100g'},
    'cabbage': {'category': 'vitamins', 'calories': 25, 'unit': '100g'},
    'cauliflower': {'category': 'vitamins', 'calories': 25, 'unit': '100g'},
    'celery': {'category': 'vitamins', 'calories': 14, 'unit': '100g'},
    'mushroom': {'category': 'vitamins', 'calories': 22, 'unit': '100g'},
    'mushrooms': {'category': 'vitamins', 'calories': 22, 'unit': '100g'},
    'zucchini': {'category': 'vitamins', 'calories': 17, 'unit': '100g'},
    'squash': {'category': 'vitamins', 'calories': 40, 'unit': '100g'},
    'pumpkin': {'category': 'vitamins', 'calories': 26, 'unit': '100g'},
    'green beans': {'category': 'vitamins', 'calories': 31, 'unit': '100g'},
    'peas': {'category': 'vitamins', 'calories': 81, 'unit': '100g'},
    'asparagus': {'category': 'vitamins', 'calories': 20, 'unit': '100g'},
    'eggplant': {'category': 'vitamins', 'calories': 25, 'unit': '100g'},
    'brussels sprouts': {'category': 'vitamins', 'calories': 43, 'unit': '100g'},
    'kale': {'category': 'vitamins', 'calories': 49, 'unit': '100g'},
    'beet': {'category': 'vitamins', 'calories': 43, 'unit': '100g'},
    'beets': {'category': 'vitamins', 'calories': 43, 'unit': '100g'},
    'radish': {'category': 'vitamins', 'calories': 16, 'unit': '100g'},
    'radishes': {'category': 'vitamins', 'calories': 16, 'unit': '100g'},
    
    # Common Dishes and Meals
    'sandwich': {'category': 'carbohydrates', 'calories': 250, 'unit': '1 serving'},
    'taco': {'category': 'carbohydrates', 'calories': 200, 'unit': '1 serving'},
    'burrito': {'category': 'carbohydrates', 'calories': 400, 'unit': '1 serving'},
    'sushi': {'category': 'carbohydrates', 'calories': 200, 'unit': '1 roll'},
    'ramen': {'category': 'carbohydrates', 'calories': 400, 'unit': '1 bowl'},
    'soup': {'category': 'carbohydrates', 'calories': 100, 'unit': '1 cup'},
    'chicken soup': {'category': 'proteins', 'calories': 80, 'unit': '1 cup'},
    'vegetable soup': {'category': 'vitamins', 'calories': 60, 'unit': '1 cup'},
    'stew': {'category': 'proteins', 'calories': 150, 'unit': '1 cup'},
    'curry': {'category': 'carbohydrates', 'calories': 200, 'unit': '1 cup'},
    'chicken curry': {'category': 'proteins', 'calories': 180, 'unit': '1 cup'},
    'pasta sauce': {'category': 'carbohydrates', 'calories': 70, 'unit': '100g'},
    'tomato sauce': {'category': 'vitamins', 'calories': 29, 'unit': '100g'},
    
    # Beverages
    'water': {'category': 'vitamins', 'calories': 0, 'unit': '100ml'},
    'coffee': {'category': 'vitamins', 'calories': 2, 'unit': '100ml'},
    'tea': {'category': 'vitamins', 'calories': 2, 'unit': '100ml'},
    'green tea': {'category': 'vitamins', 'calories': 2, 'unit': '100ml'},
    'juice': {'category': 'vitamins', 'calories': 45, 'unit': '100ml'},
    'orange juice': {'category': 'vitamins', 'calories': 45, 'unit': '100ml'},
    'apple juice': {'category': 'vitamins', 'calories': 46, 'unit': '100ml'},
    'soda': {'category': 'carbohydrates', 'calories': 41, 'unit': '100ml'},
    'coke': {'category': 'carbohydrates', 'calories': 41, 'unit': '100ml'},
    'pepsi': {'category': 'carbohydrates', 'calories': 41, 'unit': '100ml'},
    'beer': {'category': 'carbohydrates', 'calories': 43, 'unit': '100ml'},
    'wine': {'category': 'carbohydrates', 'calories': 85, 'unit': '100ml'},
    'red wine': {'category': 'carbohydrates', 'calories': 85, 'unit': '100ml'},
    'white wine': {'category': 'carbohydrates', 'calories': 82, 'unit': '100ml'},
    'smoothie': {'category': 'vitamins', 'calories': 90, 'unit': '100ml'},
    'protein shake': {'category': 'proteins', 'calories': 120, 'unit': '100ml'},
}

def get_food_info(food_name):
    """Get food information from the database"""
    food_name_lower = food_name.lower().strip()
    
    # Direct match
    if food_name_lower in FOOD_DATABASE:
        return FOOD_DATABASE[food_name_lower]
    
    # Partial match - check if food name contains any database key
    for key, info in FOOD_DATABASE.items():
        if key in food_name_lower or food_name_lower in key:
            return info
    
    # If no match found, return None
    return None

def estimate_calories(food_name, default_calories=100):
    """Estimate calories for a food item"""
    food_info = get_food_info(food_name)
    if food_info:
        return food_info['calories']
    return default_calories

def categorize_food_enhanced(food_name):
    """Enhanced food categorization using the database"""
    food_info = get_food_info(food_name)
    if food_info:
        return food_info['category']
    
    # Fallback to keyword-based categorization
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

def get_all_foods_by_category():
    """Get all foods organized by category"""
    foods_by_category = {
        'proteins': [],
        'carbohydrates': [],
        'vitamins': []
    }
    
    for food_name, info in FOOD_DATABASE.items():
        category = info['category']
        if category in foods_by_category:
            foods_by_category[category].append({
                'name': food_name,
                'calories': info['calories'],
                'unit': info['unit']
            })
    
    # Sort each category alphabetically
    for category in foods_by_category:
        foods_by_category[category].sort(key=lambda x: x['name'])
    
    return foods_by_category

def list_all_foods():
    """Get a simple list of all food names"""
    return sorted(list(FOOD_DATABASE.keys()))
