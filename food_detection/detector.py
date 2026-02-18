from PIL import Image
import numpy as np

from nutrition.nutrition_db import get_nutrition
from utils.helpers import health_score


def detect_food(img_path):

    img = Image.open(img_path).convert("RGB").resize((128, 128))
    arr = np.array(img)

    # --- basic color stats ---
    mean_rgb = arr.mean(axis=(0, 1))
    r, g, b = mean_rgb

    brightness = arr.mean()
    green_ratio = g / (r + g + b + 1e-6)

    # --- simple rules ---
    if green_ratio > 0.38:
        food = "salad"

    elif brightness > 190:
        food = "rice"

    elif r > 150 and g > 120 and b < 110:
        food = "pancakes"

    elif r > g and r > b and brightness < 160:
        food = "fried_rice"

    elif brightness < 120:
        food = "chocolate_cake"

    else:
        food = "pizza"

    confidence = 0.82

    nutrition = get_nutrition(food) or {
        "calories": 250,
        "protein": 7,
        "carbs": 35
    }

    score = health_score(nutrition)

    return {
        "food": food,
        "confidence": confidence,
        "top3": [
            {"food": food, "confidence": confidence}
        ],
        "nutrition": nutrition,
        "health_score": score
    }
