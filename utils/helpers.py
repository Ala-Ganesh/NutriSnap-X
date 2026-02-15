def calorie_goal(user):

    base = 2000

    g = (user.goal or "").lower()

    if g == "weight_loss":
        return 1600

    if g == "weight_gain":
        return 2400

    if g == "gym":
        return 2800

    if g == "senior":
        return 1800

    return base
def protein_target(user):

    g = (user.goal or "").lower()

    if g == "gym":
        return 120

    if g == "weight_gain":
        return 100

    if g == "weight_loss":
        return 70

    return 60

def suggestion(nutrition):
    if nutrition["protein"] < 5:
        return "Protein is low — consider eggs, dal, paneer."

    if nutrition["carbs"] > 40:
        return "High carbs — reduce rice/bread portion."

    return "Meal looks balanced 👍"
def health_score(nutrition):

    cal = nutrition.get("calories", 0)
    prot = nutrition.get("protein", 0)
    carbs = nutrition.get("carbs", 0)

    # --- protein score (max 40) ---
    if prot >= 20:
        p_score = 40
    elif prot >= 10:
        p_score = 30
    elif prot >= 5:
        p_score = 20
    else:
        p_score = 10

    # --- calorie score (max 30) ---
    if cal <= 250:
        c_score = 30
    elif cal <= 400:
        c_score = 22
    elif cal <= 600:
        c_score = 14
    else:
        c_score = 6

    # --- carb balance (max 30) ---
    if carbs <= 20:
        carb_score = 30
    elif carbs <= 40:
        carb_score = 22
    elif carbs <= 60:
        carb_score = 14
    else:
        carb_score = 6

    total = p_score + c_score + carb_score
    return total
def smart_alerts(user, today_cal, today_protein):

    alerts = []

    goal_cal = calorie_goal(user)

    if today_cal > goal_cal:
        alerts.append("⚠️ Daily calorie limit exceeded")

    if today_protein < 40:
        alerts.append("⚠️ Protein intake is low today")

    if today_cal < goal_cal * 0.5:
        alerts.append("ℹ️ You are far below calorie target")

    return alerts
def meal_suggestions(user, nutrition):

    tips = []

    if nutrition["protein"] < 8:
        tips.append("Add protein sources like eggs, dal, paneer")

    if nutrition["carbs"] > 40:
        tips.append("Balance with fiber or vegetables")

    if user.goal == "weight_loss":
        tips.append("Prefer grilled / low-oil foods")

    if user.goal == "muscle_gain":
        tips.append("Increase protein portions")

    return tips
def weekly_limits(user):

    daily_goal = calorie_goal(user)

    return {
        "cal_limit": daily_goal * 7,
        "protein_min": 50 * 7,
        "carb_limit": 300 * 7
    }
def weekly_limit_alerts(week_cal, week_prot, week_carbs, limits):

    alerts = []

    if week_cal > limits["cal_limit"]:
        alerts.append("🚨 Weekly calories exceeded healthy limit")

    if week_prot < limits["protein_min"]:
        alerts.append("⚠️ Weekly protein below recommended level")

    if week_carbs > limits["carb_limit"]:
        alerts.append("⚠️ Weekly carbs too high")

    return alerts
def personalization_advice(user, week_cal, week_prot, week_avg_score):

    tips = []

    goal = user.goal.lower()

    # --- calorie pattern ---
    if week_cal > calorie_goal(user) * 7:
        tips.append("Reduce portion sizes next week")

    if week_cal < calorie_goal(user) * 7 * 0.6:
        tips.append("Increase meal frequency for better nutrition")

    # --- protein pattern ---
    if week_prot < 50 * 7:
        tips.append("Add protein-rich foods daily")

    # --- health score pattern ---
    if week_avg_score < 50:
        tips.append("Choose grilled, low-oil foods more often")
    elif week_avg_score > 75:
        tips.append("Great meal quality trend — maintain it")

    # --- goal specific ---
    if "loss" in goal:
        tips.append("Prefer low-carb dinners")

    if "gain" in goal or "gym" in goal:
        tips.append("Add post-meal protein sources")

    return tips
