from PIL import Image
import random

from nutrition.nutrition_db import get_nutrition
from utils.helpers import health_score
from food_detection.food101_labels import LABELS


def detect_food(img_path):

    # open just to validate image
    Image.open(img_path).convert("RGB")

    # lightweight mock prediction (demo-safe)
    food = random.choice(LABELS[:20])
    confidence = round(random.uniform(0.75, 0.95), 3)

    nutrition = get_nutrition(food) or {
        "calories": 220,
        "protein": 8,
        "carbs": 30
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
