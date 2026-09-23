"""
NutriSnap-X - Local Nutrition Database
Per-100g values for common foods used in mock detection
"""

NUTRITION_DB = {
    "pizza": {
        "food_name": "Pizza (Cheese)",
        "calories": 266,
        "protein": 11.4,
        "carbs": 32.9,
        "fat": 9.8,
        "fibre": 2.3,
        "serving_g": 100
    },
    "burger": {
        "food_name": "Beef Burger",
        "calories": 295,
        "protein": 17.0,
        "carbs": 24.0,
        "fat": 14.0,
        "fibre": 1.2,
        "serving_g": 100
    },
    "salad": {
        "food_name": "Garden Salad",
        "calories": 20,
        "protein": 1.5,
        "carbs": 3.8,
        "fat": 0.3,
        "fibre": 2.0,
        "serving_g": 100
    },
    "rice": {
        "food_name": "Cooked White Rice",
        "calories": 130,
        "protein": 2.7,
        "carbs": 28.0,
        "fat": 0.3,
        "fibre": 0.4,
        "serving_g": 100
    },
    "pasta": {
        "food_name": "Cooked Pasta",
        "calories": 158,
        "protein": 5.8,
        "carbs": 31.0,
        "fat": 0.9,
        "fibre": 1.8,
        "serving_g": 100
    },
    "apple": {
        "food_name": "Apple",
        "calories": 52,
        "protein": 0.3,
        "carbs": 13.8,
        "fat": 0.2,
        "fibre": 2.4,
        "serving_g": 182
    },
    "banana": {
        "food_name": "Banana",
        "calories": 89,
        "protein": 1.1,
        "carbs": 22.8,
        "fat": 0.3,
        "fibre": 2.6,
        "serving_g": 118
    },
    "chicken": {
        "food_name": "Grilled Chicken Breast",
        "calories": 165,
        "protein": 31.0,
        "carbs": 0.0,
        "fat": 3.6,
        "fibre": 0.0,
        "serving_g": 100
    },
    "egg": {
        "food_name": "Boiled Egg",
        "calories": 78,
        "protein": 6.3,
        "carbs": 0.6,
        "fat": 5.3,
        "fibre": 0.0,
        "serving_g": 50
    },
    "sandwich": {
        "food_name": "Chicken Sandwich",
        "calories": 284,
        "protein": 15.0,
        "carbs": 36.0,
        "fat": 7.5,
        "fibre": 2.0,
        "serving_g": 150
    },
    "sushi": {
        "food_name": "Sushi Roll",
        "calories": 200,
        "protein": 9.0,
        "carbs": 38.0,
        "fat": 1.5,
        "fibre": 1.0,
        "serving_g": 150
    },
    "oatmeal": {
        "food_name": "Oatmeal",
        "calories": 166,
        "protein": 5.9,
        "carbs": 32.0,
        "fat": 3.6,
        "fibre": 4.0,
        "serving_g": 240
    },
    "yogurt": {
        "food_name": "Greek Yogurt",
        "calories": 59,
        "protein": 10.0,
        "carbs": 3.6,
        "fat": 0.4,
        "fibre": 0.0,
        "serving_g": 100
    },
    "soup": {
        "food_name": "Vegetable Soup",
        "calories": 60,
        "protein": 3.5,
        "carbs": 12.0,
        "fat": 0.5,
        "fibre": 3.0,
        "serving_g": 240
    },
    "steak": {
        "food_name": "Beef Steak",
        "calories": 271,
        "protein": 26.0,
        "carbs": 0.0,
        "fat": 18.0,
        "fibre": 0.0,
        "serving_g": 100
    },
    "default": {
        "food_name": "Mixed Dish",
        "calories": 220,
        "protein": 8.0,
        "carbs": 28.0,
        "fat": 8.0,
        "fibre": 2.5,
        "serving_g": 200
    }
}


def get_nutrition(food_key: str) -> dict:
    """Fetch nutrition data by food key, fallback to default."""
    return NUTRITION_DB.get(food_key.lower(), NUTRITION_DB['default'])
