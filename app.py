"""
NutriSnap-X - AI-Based Food Nutrition Analysis Web Application
Main application entry point
"""

import os
import json
import base64
import random
# NutriSnap-X deployment verification update
from datetime import datetime, timedelta, date

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify, session, send_file
)
from flask_login import (
    login_required, current_user, login_user, logout_user
)
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import requests

from extensions import db, login_manager
from database.models import User, FoodLog, BarcodeLog
from nutrition.nutrition_db import NUTRITION_DB
from utils.helpers import (
    calculate_health_score,
    get_weekly_average,
    allowed_file,
    mock_food_detection,
    generate_pdf_report,
    get_ai_suggestion
)

# ─── App Factory ──────────────────────────────────────────────────────────────

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'nutrisnap-x-secret-2024-change-in-prod')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + os.path.join(app.instance_path, 'nutrisnap.db')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()

# ─── User Loader ──────────────────────────────────────────────────────────────

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─── Main Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth_bp.login'))


@app.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    today_logs = FoodLog.query.filter_by(
        user_id=current_user.id
    ).filter(
        db.func.date(FoodLog.logged_at) == today
    ).all()

    total_calories = sum(log.calories for log in today_logs)
    total_protein  = sum(log.protein  for log in today_logs)
    total_carbs    = sum(log.carbs    for log in today_logs)
    total_fibre    = sum(log.fibre    for log in today_logs)

    daily_goal   = current_user.daily_calorie_goal or 2000
    protein_goal = current_user.protein_goal       or 60
    fibre_goal   = current_user.fibre_goal         or 30

    health_score   = calculate_health_score(total_calories, total_protein, total_fibre, daily_goal)
    weekly_avg     = get_weekly_average(current_user.id)
    cal_percentage = min(int((total_calories / daily_goal) * 100), 100) if daily_goal else 0

    # Smart alert
    alert = None
    if total_calories > daily_goal * 0.9:
        alert = {'type': 'warning', 'msg': f'You\'re at {cal_percentage}% of your daily calorie goal. Consider lighter meals.'}
    elif total_calories == 0:
        alert = {'type': 'info', 'msg': 'No food logged today. Start tracking to get your health score!'}

    # Personalized tips (max 2)
    tips = []
    if total_protein < protein_goal * 0.5:
        tips.append('Your protein intake is low — try adding eggs, legumes, or Greek yogurt.')
    if total_fibre < fibre_goal * 0.5:
        tips.append('Boost fibre with fruits, vegetables, or whole grains.')
    tips = tips[:2]

    recent_logs = FoodLog.query.filter_by(user_id=current_user.id).order_by(
        FoodLog.logged_at.desc()
    ).limit(5).all()

    return render_template(
        'dashboard.html',
        total_calories=total_calories,
        total_protein=round(total_protein, 1),
        total_carbs=round(total_carbs, 1),
        total_fibre=round(total_fibre, 1),
        daily_goal=daily_goal,
        protein_goal=protein_goal,
        fibre_goal=fibre_goal,
        cal_percentage=cal_percentage,
        protein_percentage=min(int((total_protein / protein_goal) * 100), 100) if protein_goal else 0,
        fibre_percentage=min(int((total_fibre / fibre_goal) * 100), 100) if fibre_goal else 0,
        health_score=health_score,
        weekly_avg=weekly_avg,
        alert=alert,
        tips=tips,
        recent_logs=recent_logs,
        today=today
    )


# ─── Food Image Analysis ──────────────────────────────────────────────────────

@app.route('/analyze', methods=['GET', 'POST'])
@login_required
def analyze():
    if request.method == 'POST':
        if 'food_image' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(request.url)

        file = request.files['food_image']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename  = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename  = timestamp + filename
            filepath  = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Mock food detection (replace with real model)
            detection = mock_food_detection(filename)

            # Store in DB
            log = FoodLog(
                user_id   = current_user.id,
                food_name = detection['food_name'],
                calories  = detection['calories'],
                protein   = detection['protein'],
                carbs     = detection['carbs'],
                fat       = detection['fat'],
                fibre     = detection['fibre'],
                source    = 'image',
                image_url = f'/static/uploads/{filename}'
            )
            db.session.add(log)
            db.session.commit()

            flash(f'"{detection["food_name"]}" detected and logged successfully!', 'success')
            return render_template('analyze_result.html', detection=detection, filename=filename)

        flash('Invalid file type. Please upload JPG, PNG, or WEBP.', 'danger')
        return redirect(request.url)

    return render_template('analyze.html')


# ─── Barcode Scanner ──────────────────────────────────────────────────────────

@app.route('/barcode')
@login_required
def barcode():
    return render_template('barcode.html')


@app.route('/api/barcode/lookup', methods=['POST'])
@login_required
def barcode_lookup():
    data    = request.get_json()
    barcode = data.get('barcode', '').strip()

    if not barcode:
        return jsonify({'success': False, 'error': 'No barcode provided'}), 400

    # Try OpenFoodFacts
    try:
        off_url = f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json'
        resp    = requests.get(off_url, timeout=8)
        off_data = resp.json()

        if off_data.get('status') == 1:
            product = off_data['product']
            nutriments = product.get('nutriments', {})

            calories = nutriments.get('energy-kcal_100g', nutriments.get('energy-kcal', 0)) or 0
            protein  = nutriments.get('proteins_100g', 0) or 0
            carbs    = nutriments.get('carbohydrates_100g', 0) or 0
            fat      = nutriments.get('fat_100g', 0) or 0
            fibre    = nutriments.get('fiber_100g', 0) or 0
            sugar    = nutriments.get('sugars_100g', 0) or 0
            sodium   = nutriments.get('sodium_100g', 0) or 0

            food_name = product.get('product_name', 'Unknown Product')
            brand     = product.get('brands', '')
            image_url = product.get('image_url', '')

            health_indicator = _health_indicator(calories, fat, sugar, sodium)
            ai_suggestion    = get_ai_suggestion(food_name, calories, protein, carbs, fat, fibre)

            # Log it
            log = BarcodeLog(
                user_id   = current_user.id,
                barcode   = barcode,
                food_name = food_name,
                brand     = brand,
                calories  = float(calories),
                protein   = float(protein),
                carbs     = float(carbs),
                fat       = float(fat),
                fibre     = float(fibre),
                source    = 'barcode'
            )
            db.session.add(log)

            food_log = FoodLog(
                user_id   = current_user.id,
                food_name = f'{brand} {food_name}'.strip() if brand else food_name,
                calories  = float(calories),
                protein   = float(protein),
                carbs     = float(carbs),
                fat       = float(fat),
                fibre     = float(fibre),
                source    = 'barcode'
            )
            db.session.add(food_log)
            db.session.commit()

            return jsonify({
                'success'          : True,
                'source'           : 'openfoodfacts',
                'food_name'        : food_name,
                'brand'            : brand,
                'image_url'        : image_url,
                'calories'         : round(float(calories), 1),
                'protein'          : round(float(protein), 1),
                'carbs'            : round(float(carbs), 1),
                'fat'              : round(float(fat), 1),
                'fibre'            : round(float(fibre), 1),
                'sugar'            : round(float(sugar), 1),
                'sodium'           : round(float(sodium), 4),
                'health_indicator' : health_indicator,
                'ai_suggestion'    : ai_suggestion
            })

    except requests.exceptions.RequestException:
        pass

    # AI Fallback
    ai_estimate = _ai_barcode_fallback(barcode)
    return jsonify(ai_estimate)


def _health_indicator(calories, fat, sugar, sodium):
    score = 0
    if calories > 400: score += 2
    elif calories > 200: score += 1
    if fat > 20: score += 2
    elif fat > 10: score += 1
    if sugar > 20: score += 2
    elif sugar > 10: score += 1
    if sodium > 0.6: score += 2
    elif sodium > 0.3: score += 1

    if score <= 2:   return 'green'
    elif score <= 5: return 'yellow'
    else:            return 'red'


def _ai_barcode_fallback(barcode):
    # Rule-based fallback estimate
    estimates = [
        {'food_name': 'Energy Bar', 'calories': 250, 'protein': 8, 'carbs': 35, 'fat': 9, 'fibre': 4},
        {'food_name': 'Packaged Snack', 'calories': 180, 'protein': 3, 'carbs': 28, 'fat': 7, 'fibre': 1},
        {'food_name': 'Breakfast Cereal', 'calories': 120, 'protein': 3, 'carbs': 25, 'fat': 1, 'fibre': 3},
    ]
    est = random.choice(estimates)
    est.update({
        'success': True,
        'source': 'ai_fallback',
        'brand': '',
        'image_url': '',
        'sugar': round(est['carbs'] * 0.3, 1),
        'sodium': 0.3,
        'health_indicator': _health_indicator(est['calories'], est['fat'], est['carbs'] * 0.3, 0.3),
        'ai_suggestion': get_ai_suggestion(est['food_name'], est['calories'], est['protein'], est['carbs'], est['fat'], est['fibre'])
    })
    return est


@app.route('/api/barcode/manual', methods=['POST'])
@login_required
def barcode_manual():
    data      = request.get_json()
    food_name = data.get('food_name', 'Unknown')
    calories  = float(data.get('calories', 0))
    protein   = float(data.get('protein', 0))
    carbs     = float(data.get('carbs', 0))
    fat       = float(data.get('fat', 0))
    fibre     = float(data.get('fibre', 0))

    log = FoodLog(
        user_id=current_user.id,
        food_name=food_name,
        calories=calories,
        protein=protein,
        carbs=carbs,
        fat=fat,
        fibre=fibre,
        source='manual'
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'success': True, 'message': f'{food_name} logged manually.'})


# ─── Analytics ────────────────────────────────────────────────────────────────

@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')


@app.route('/api/analytics/data')
@login_required
def analytics_data():
    days  = int(request.args.get('days', 7))
    end   = datetime.now()
    start = end - timedelta(days=days - 1)

    labels   = []
    calories = []
    protein  = []
    carbs    = []

    for i in range(days):
        day = (start + timedelta(days=i)).date()
        labels.append(day.strftime('%b %d'))

        logs = FoodLog.query.filter_by(user_id=current_user.id).filter(
            db.func.date(FoodLog.logged_at) == day
        ).all()

        calories.append(round(sum(l.calories for l in logs), 1))
        protein.append(round(sum(l.protein for l in logs), 1))
        carbs.append(round(sum(l.carbs for l in logs), 1))

    return jsonify({
        'labels'  : labels,
        'calories': calories,
        'protein' : protein,
        'carbs'   : carbs
    })


# ─── PDF Report ───────────────────────────────────────────────────────────────

@app.route('/report')
@login_required
def report():
    return render_template('report.html')


@app.route('/api/report/generate')
@login_required
def generate_report():
    end   = datetime.now()
    start = end - timedelta(days=6)

    logs = FoodLog.query.filter_by(user_id=current_user.id).filter(
        FoodLog.logged_at >= start
    ).order_by(FoodLog.logged_at.desc()).all()

    pdf_path = generate_pdf_report(current_user, logs, start, end)
    return send_file(pdf_path, as_attachment=True, download_name='NutriSnap_Weekly_Report.pdf')


# ─── AI Chatbot ───────────────────────────────────────────────────────────────

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')


@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    data    = request.get_json()
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Empty message'}), 400

    openai_key = os.environ.get('OPENAI_API_KEY', '')

    if openai_key and openai_key != 'your-openai-key-here':
        try:
            headers = {
                'Authorization': f'Bearer {openai_key}',
                'Content-Type' : 'application/json'
            }
            payload = {
                'model'   : 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role'   : 'system',
                        'content': (
                            'You are NutriBot, an expert AI nutrition assistant for NutriSnap-X. '
                            'You provide concise, evidence-based nutritional advice. '
                            'Focus on practical tips about food, macros, and healthy eating habits. '
                            'Keep responses under 150 words.'
                        )
                    },
                    {'role': 'user', 'content': message}
                ],
                'max_tokens': 200
            }
            resp    = requests.post('https://api.openai.com/v1/chat/completions',
                                    headers=headers, json=payload, timeout=15)
            resp_data = resp.json()
            reply  = resp_data['choices'][0]['message']['content']
            return jsonify({'reply': reply})
        except Exception as e:
            pass

    # Fallback rule-based chatbot
    reply = _rule_based_chat(message)
    return jsonify({'reply': reply})


def _rule_based_chat(message):
    msg = message.lower()
    if any(w in msg for w in ['calorie', 'calories', 'kcal']):
        return 'Calories are units of energy. Adult daily needs range from 1600–2500 kcal depending on age, sex, and activity. Tracking consistently is key to managing weight.'
    if any(w in msg for w in ['protein', 'proteins']):
        return 'Protein is essential for muscle repair and immunity. Aim for 0.8–1.2g per kg of body weight. Good sources: eggs, lentils, chicken, tofu, Greek yogurt.'
    if any(w in msg for w in ['carb', 'carbs', 'carbohydrate']):
        return 'Carbohydrates are your primary energy source. Choose complex carbs (oats, brown rice, vegetables) over simple sugars for sustained energy.'
    if any(w in msg for w in ['fat', 'fats', 'lipid']):
        return 'Healthy fats (avocado, nuts, olive oil) are vital for brain function and hormone production. Limit saturated and trans fats.'
    if any(w in msg for w in ['fibre', 'fiber']):
        return 'Dietary fibre aids digestion and lowers cholesterol. Target 25–38g/day. Best sources: fruits, vegetables, legumes, whole grains.'
    if any(w in msg for w in ['weight', 'lose', 'loss', 'diet']):
        return 'Sustainable weight loss involves a modest calorie deficit (300–500 kcal/day), adequate protein, and regular movement. Avoid extreme crash diets.'
    if any(w in msg for w in ['water', 'hydration', 'drink']):
        return 'Staying hydrated supports metabolism and appetite control. Aim for 2–3 litres of water daily, more if active or in hot climates.'
    if any(w in msg for w in ['breakfast', 'lunch', 'dinner', 'meal']):
        return 'A balanced meal includes a protein source, complex carbs, healthy fat, and vegetables. Eating mindfully and at regular intervals supports better metabolism.'
    return 'I\'m NutriBot, your nutrition assistant! Ask me about calories, proteins, carbs, fats, fibre, hydration, or healthy eating habits. 🥗'


# ─── Food Log Management ─────────────────────────────────────────────────────

@app.route('/logs')
@login_required
def logs():
    page  = request.args.get('page', 1, type=int)
    logs_ = FoodLog.query.filter_by(user_id=current_user.id).order_by(
        FoodLog.logged_at.desc()
    ).paginate(page=page, per_page=15, error_out=False)
    return render_template('logs.html', logs=logs_)


@app.route('/api/log/delete/<int:log_id>', methods=['DELETE'])
@login_required
def delete_log(log_id):
    log = FoodLog.query.filter_by(id=log_id, user_id=current_user.id).first_or_404()
    db.session.delete(log)
    db.session.commit()
    return jsonify({'success': True})


# ─── Profile & Settings ───────────────────────────────────────────────────────

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.daily_calorie_goal = int(request.form.get('calorie_goal', 2000))
        current_user.protein_goal       = int(request.form.get('protein_goal', 60))
        current_user.fibre_goal         = int(request.form.get('fibre_goal', 30))
        current_user.full_name          = request.form.get('full_name', current_user.full_name)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html')


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port  = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
