import torch
import timm
from PIL import Image
from torchvision import transforms

from nutrition.nutrition_db import get_nutrition
from food_detection.food101_labels import LABELS
from utils.helpers import health_score


# --- load model ---
model = timm.create_model("resnet50", pretrained=False, num_classes=101)
model.load_state_dict(
    torch.load("food_detection/food101_resnet50.pth", map_location="cpu")
)
model.eval()


# --- image transform ---
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485,0.456,0.406],
        std=[0.229,0.224,0.225]
    )
])


# ✅ MAIN FUNCTION
def detect_food(img_path):

    img = Image.open(img_path).convert("RGB")
    x = transform(img).unsqueeze(0)

    with torch.no_grad():
        out = model(x)
        probs = torch.softmax(out, dim=1)[0]

    # --- top 3 predictions ---
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

    # ✅ return MUST be inside function
    return {
        "food": best_food,
        "confidence": round(best_conf, 3),
        "top3": top_list,
        "nutrition": nutrition,
        "health_score": score
    }
