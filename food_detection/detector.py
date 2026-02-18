from PIL import Image
import numpy as np

from nutrition.nutrition_db import get_nutrition
from utils.helpers import health_score


def detect_food(img_path):

    img = Image.open(img_path).convert("RGB").resize((160, 160))
    arr = np.array(img).astype(np.float32)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    mean_r = r.mean()
    mean_g = g.mean()
    mean_b = b.mean()

    brightness = arr.mean()

    # --- feature ratios ---
    green_pixels = np.mean((g > r) & (g > b))
    yellow_pixels = np.mean((r > 160) & (g > 140) & (b < 120))
    dark_pixels = np.mean(brightness < 90)

    color_std = arr.std()   # texture / variation

    # ---------- rules ----------

    # Salad → lots of green + high color variation
    if green_pixels > 0.30 and color_std > 40:
        food = "salad"

    # Pasta → yellowish + medium variation
    elif yellow_pixels > 0.25 and color_std > 25:
        food = "pasta"

    # Omelette → yellow but low variation (flat texture)
    elif yellow_pixels > 0.25 and color_std <= 25:
        food = "omelette"

    # Fried rice → warm tones + mixed colors
    elif mean_r > mean_g and mean_r > mean_b and color_std > 35:
        food = "fried_rice"

    # Cake / dessert → darker overall
    elif dark_pixels > 0.25:
        food = "chocolate_cake"

    else:
        food = "pizza"

    confidence = 0.84

    nutrition = get_nutrition(food) or {
        "calories": 260,
        "protein": 8,
        "carbs": 32
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
