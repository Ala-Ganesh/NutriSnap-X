DATA = {
    "rice": {"calories": 130, "protein": 2.5, "carbs": 28},
    "apple": {"calories": 52, "protein": 0.3, "carbs": 14},
    "banana": {"calories": 89, "protein": 1.1, "carbs": 23},
    "pizza": {"calories": 266, "protein": 11, "carbs": 33},
    "dal": {"calories": 116, "protein": 9, "carbs": 20},
    "egg": {"calories": 155, "protein": 13, "carbs": 1}
}

def get_nutrition(food):
    return DATA.get(food, {})
BARCODE_DATA = {
    "8901030865271": {
        "name": "Maggi Noodles",
        "calories": 350,
        "protein": 8,
        "carbs": 50
    },
    "8901491101833": {
        "name": "Amul Butter",
        "calories": 717,
        "protein": 1,
        "carbs": 0
    }
}

def get_barcode_nutrition(code):
    return BARCODE_DATA.get(code)
