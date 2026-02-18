from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    current_app
)

from utils.helpers import personalization_advice
from utils.helpers import weekly_limits, weekly_limit_alerts
from datetime import datetime, timedelta
from utils.helpers import smart_alerts
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import send_file
import io
from flask_login import current_user
from database.models import MealLog
import os
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from sqlalchemy import func
from nutrition.nutrition_db import get_barcode_nutrition
from utils.helpers import (
    weekly_limits,
    personalization_advice,
    health_score
)

from extensions import db
from database.models import User
import os
from flask import request, jsonify
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are NutriGenie AI — the intelligent assistant inside NutriSnap-X.
You help users with:
- food and nutrition questions
- diet and calorie doubts
- app usage help
- general knowledge questions

Answer clearly, simply, and accurately.
Avoid medical diagnosis claims.
Keep answers practical and easy to understand.
"""

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.4
        )

        answer = resp.choices[0].message.content
        return jsonify({"reply": answer})

    except Exception as e:
        return jsonify({"reply": "AI is temporarily unavailable. Please try again."})

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/")
def home():
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        age = request.form["age"]
        weight = request.form["weight"]
        height = request.form["height"]
        goal = request.form["goal"]

        # check existing user
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email already registered. Please login.")
            return redirect(url_for("auth.login"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            age=age,
            weight=weight,
            height=height,
            goal=goal
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")




@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("auth_bp.dashboard"))

    return render_template("login.html")


from utils.helpers import calorie_goal
from database.models import MealLog
from sqlalchemy import func

@auth_bp.route("/dashboard")
@login_required
def dashboard():

    from datetime import datetime, timedelta
    from utils.helpers import (
        smart_alerts,
        weekly_limits,
        weekly_limit_alerts,
        personalization_advice,
        health_score
    )

    meals = MealLog.query.filter_by(
        user_id=current_user.id
    ).all()

    # ---------- totals ----------
    total_cal = sum(m.calories for m in meals)
    total_prot = sum(m.protein for m in meals)

    goal_cal = calorie_goal(current_user)

    # ---------- weekly window ----------
    week_ago = datetime.utcnow() - timedelta(days=7)

    week_meals = [
        m for m in meals
        if m.timestamp and m.timestamp >= week_ago
    ]

    # ---------- weekly sums ----------
    week_cal = sum(m.calories for m in week_meals)
    week_prot = sum(m.protein for m in week_meals)
    week_carbs = sum(m.carbs for m in week_meals)

    days = 7 if week_meals else 1
    week_avg = week_cal / days

    # ---------- weekly health score avg ----------
    week_scores = [
        health_score({
            "calories": m.calories,
            "protein": m.protein,
            "carbs": m.carbs
        })
        for m in week_meals
    ]

    week_avg_score = sum(week_scores)/len(week_scores) if week_scores else 0

    # ---------- alerts ----------
    alerts = smart_alerts(current_user, total_cal, total_prot)

    # ---------- weekly limits ----------
    limits = weekly_limits(current_user)

    week_limit_alerts = weekly_limit_alerts(
        week_cal,
        week_prot,
        week_carbs,
        limits
    )

    # ---------- personalization ----------
    personal_tips = personalization_advice(
        current_user,
        week_cal,
        week_prot,
        week_avg_score
    )

    return render_template(
        "dashboard.html",
        total=round(total_cal,1),
        goal=round(goal_cal,1),
        alerts=alerts,

        week_cal=round(week_cal,1),
        week_prot=round(week_prot,1),
        week_count=len(week_meals),
        week_avg=round(week_avg,1),

        week_limit_alerts=week_limit_alerts,
        week_cal_limit=round(limits["cal_limit"],1),

        personal_tips=personal_tips,
        week_avg_score=round(week_avg_score,1)
    )






@auth_bp.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():

    if request.method == "POST":

        file = request.files["food_image"]

        if file:
            filename = secure_filename(file.filename)
            upload_path = os.path.join("static/uploads", filename)
            file.save(upload_path)

            from food_detection.detector import detect_food
            from utils.helpers import meal_suggestions
            from database.models import MealLog
            from flask_login import current_user

            result = detect_food(upload_path)

            # --- save meal ---
            meal = MealLog(
                user_id=current_user.id,
                food=result["food"],
                calories=result["nutrition"]["calories"],
                protein=result["nutrition"]["protein"],
                carbs=result["nutrition"]["carbs"],
                image=filename
            )

            db.session.add(meal)
            db.session.commit()

            # --- suggestions ---
            tips = meal_suggestions(current_user, result["nutrition"])

            return render_template(
                "result.html",
                result=result,
                image=filename,
                tips=tips
            )

    return render_template("analyze.html")



    meals = MealLog.query.filter_by(user_id=current_user.id).all()

    foods = [m.food for m in meals]
    calories = [m.calories for m in meals]
    protein = [m.protein for m in meals]
    carbs = [m.carbs for m in meals]

    return render_template(
        "analytics.html",
        foods=foods,
        calories=calories,
        protein=protein,
        carbs=carbs
    )

@auth_bp.route("/barcode", methods=["GET", "POST"])
@login_required
def barcode():

    if request.method == "POST":
        code = request.form["barcode"]
        data = get_barcode_nutrition(code)

        if data:
            meal = MealLog(
                user_id=current_user.id,
                food=data["name"],
                calories=data["calories"],
                protein=data["protein"],
                carbs=data["carbs"],
                image="barcode"
            )

            db.session.add(meal)
            db.session.commit()

            return render_template("barcode_result.html", data=data, code=code)

        return "Barcode not found in dataset"

    return render_template("barcode_scan.html")

@auth_bp.route("/report")
@login_required
def report():

    meals = MealLog.query.filter_by(user_id=current_user.id).all()

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    y = 750
    c.setFont("Helvetica", 12)

    c.drawString(50, y, "NutriSnap-X Nutrition Report")
    y -= 30

    c.drawString(50, y, f"User: {current_user.name}")
    y -= 20
    c.drawString(50, y, f"Goal: {current_user.goal}")
    y -= 30

    total_cal = 0

    for m in meals:
        line = f"{m.food}  | Cal:{m.calories}  Prot:{m.protein}  Carb:{m.carbs}"
        c.drawString(50, y, line)
        total_cal += m.calories
        y -= 20

        if y < 80:
            c.showPage()
            y = 750

    y -= 20
    c.drawString(50, y, f"Total Calories: {round(total_cal,1)}")

    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="nutrition_report.pdf",
        mimetype="application/pdf"
    )

@auth_bp.route("/report/weekly")
@login_required
def weekly_report():

    meals = MealLog.query.filter_by(
        user_id=current_user.id
    ).all()

    week_ago = datetime.utcnow() - timedelta(days=7)

    week_meals = [
        m for m in meals
        if m.timestamp and m.timestamp >= week_ago
    ]

    week_cal = sum(m.calories for m in week_meals)
    week_prot = sum(m.protein for m in week_meals)
    week_carbs = sum(m.carbs for m in week_meals)

    days = 7 if week_meals else 1
    week_avg = week_cal / days

    scores = [
        health_score({
            "calories": m.calories,
            "protein": m.protein,
            "carbs": m.carbs
        })
        for m in week_meals
    ]

    week_avg_score = sum(scores)/len(scores) if scores else 0

    limits = weekly_limits(current_user)

    tips = personalization_advice(
        current_user,
        week_cal,
        week_prot,
        week_avg_score
    )

        # ---------- PDF ----------
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    now = datetime.now().strftime("%d-%m-%Y %H:%M")

    y = 780

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "NutriSnap-X AI Nutrition Report")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Generated on: {now}")
    y -= 25

    # User Info
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "User Information")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"User: {current_user.name}")
    y -= 18
    c.drawString(50, y, f"Goal Profile: {current_user.goal}")
    y -= 18
    c.drawString(50, y, "Report Type: Weekly Nutrition Intelligence")
    y -= 25

    # Metrics
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Weekly Metrics")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Total Calories: {round(week_cal,1)}")
    y -= 18
    c.drawString(50, y, f"Total Protein: {round(week_prot,1)} g")
    y -= 18
    c.drawString(50, y, f"Total Carbs: {round(week_carbs,1)} g")
    y -= 18
    c.drawString(50, y, f"Average / Day: {round(week_avg,1)}")
    y -= 18
    c.drawString(50, y, f"Health Score Avg: {round(week_avg_score,1)} / 100")
    y -= 25

    # Limits
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Healthy Limits Reference")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Weekly Calorie Limit: {round(limits['cal_limit'],1)}")
    y -= 25

    # Advice
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Personalized AI Advice")
    y -= 20

    c.setFont("Helvetica", 11)

    for t in tips:
        if y < 80:
            c.showPage()
            y = 780
            c.setFont("Helvetica", 11)

        c.drawString(50, y, f"- {t}")
        y -= 18

    y -= 20

    # Certification
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(
        50, y,
        "This report is automatically generated by NutriSnap-X AI Nutrition System."
    )
    y -= 30

    # Signature
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "System Signature: ______________________")

    c.save()
    buffer.seek(0)


    return send_file(
        buffer,
        as_attachment=True,
        download_name="weekly_report.pdf",
        mimetype="application/pdf"
    )

@auth_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))
