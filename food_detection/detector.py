from PIL import Image
from torchvision import transforms

from nutrition.nutrition_db import get_nutrition
from food_detection.food101_labels import LABELS
from utils.helpers import health_score


# -------------------------------
# Lazy Model Loader
# -------------------------------

model = None

def get_model():
    global model
    if model is None:
        print("🔄 Loading food model...")
        import torch
        import timm

        timm.create_model("mobilenetv3_small_100", ...)
        m.load_state_dict(
            torch.load("food_detection/food101_resnet50.pth", map_location="cpu")
        )
        m.eval()

        model = m
        print("✅ Model loaded")

    return model


# -------------------------------
# Image Transform
# -------------------------------

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# -------------------------------
# Main Detection Function
# -------------------------------

def detect_food(img_path):

    import torch

    img = Image.open(img_path).convert("RGB")
    x = transform(img).unsqueeze(0)

    mdl = get_model()

    with torch.no_grad():
        out = mdl(x)
        probs = torch.softmax(out, dim=1)[0]

    # Top 3 predictions
    top_probs, top_idxs = torch.topk(probs, 3)

    top_list = []
    for p, i in zip(top_probs, top_idxs):
        label = LABELS[i.item() % len(LABELS)]
        top_list.append({
            "food": label,
            "confidence": float(p)
        })

    best_food = top_list[0]["food"]
    best_conf = top_list[0]["confidence"]

    nutrition = get_nutrition(best_food) or {
        "calories": 200,
        "protein": 6,
        "carbs": 25
    }

    score = health_score(nutrition)

    return {
        "food": best_food,
        "confidence": round(best_conf, 3),
        "top3": top_list,
        "nutrition": nutrition,
        "health_score": score
    }
