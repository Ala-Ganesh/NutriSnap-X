"""
NutriSnap-X - Utility Helpers
Shared utility functions used across the application
"""

import os
import random
import tempfile
from datetime import datetime, timedelta, date

from nutrition.nutrition_db import NUTRITION_DB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}


def allowed_file(filename: str) -> bool:
    """Check if uploaded file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def mock_food_detection(filename: str) -> dict:
    """
    Mock food detection using filename heuristics + random selection.
    Replace this with a real TensorFlow/MobileNetV2 model for production.
    """
    name_lower = filename.lower()
    detected_key = 'default'

    for key in NUTRITION_DB:
        if key in name_lower and key != 'default':
            detected_key = key
            break

    if detected_key == 'default':
        # Random selection from DB for demo purposes
        keys = [k for k in NUTRITION_DB if k != 'default']
        detected_key = random.choice(keys)

    nutrition = NUTRITION_DB[detected_key].copy()
    nutrition['confidence'] = round(random.uniform(0.78, 0.97), 2)
    nutrition['detected_key'] = detected_key
    return nutrition


def calculate_health_score(calories: float, protein: float, fibre: float, daily_goal: int) -> int:
    """
    Calculate a 0-100 health score based on macros and calorie adherence.
    """
    score = 50  # Baseline

    if daily_goal > 0:
        cal_ratio = calories / daily_goal
        if 0.7 <= cal_ratio <= 1.0:
            score += 20
        elif 0.5 <= cal_ratio < 0.7:
            score += 10
        elif cal_ratio > 1.1:
            score -= 10

    protein_score = min(protein / 60, 1.0) * 15
    score += int(protein_score)

    fibre_score = min(fibre / 30, 1.0) * 15
    score += int(fibre_score)

    return max(0, min(100, score))


def get_weekly_average(user_id: int) -> dict:
    """Calculate weekly average calories, protein, carbs."""
    from extensions import db
    from database.models import FoodLog

    end   = datetime.now()
    start = end - timedelta(days=6)

    totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'days': 0}

    for i in range(7):
        day  = (start + timedelta(days=i)).date()
        logs = FoodLog.query.filter_by(user_id=user_id).filter(
            db.func.date(FoodLog.logged_at) == day
        ).all()

        if logs:
            totals['calories'] += sum(l.calories for l in logs)
            totals['protein']  += sum(l.protein  for l in logs)
            totals['carbs']    += sum(l.carbs    for l in logs)
            totals['days']     += 1

    days = totals['days'] or 1
    return {
        'avg_calories': round(totals['calories'] / days, 1),
        'avg_protein' : round(totals['protein']  / days, 1),
        'avg_carbs'   : round(totals['carbs']    / days, 1),
        'days_tracked': totals['days']
    }


def get_ai_suggestion(food_name: str, calories: float, protein: float,
                       carbs: float, fat: float, fibre: float) -> str:
    """
    Rule-based AI suggestion for a food item.
    Can be replaced with OpenAI API call.
    """
    suggestions = []

    if calories > 400:
        suggestions.append(f'High calorie item ({int(calories)} kcal). Consider a smaller portion.')
    elif calories < 50:
        suggestions.append(f'Low calorie choice! Great for a light snack.')

    if carbs > 50:
        suggestions.append('High in carbs — pair with protein to slow glucose absorption.')

    if fat > 20:
        suggestions.append('High fat content — prefer unsaturated fats like those in nuts and avocados.')

    if protein > 15:
        suggestions.append(f'Excellent protein source ({int(protein)}g)! Supports muscle health.')

    if fibre > 5:
        suggestions.append('Rich in dietary fibre — great for digestive health!')
    elif fibre < 1:
        suggestions.append('Low fibre — add vegetables or whole grains to your meal.')

    if not suggestions:
        suggestions.append(f'{food_name} is a balanced option. Track portion size for best results.')

    return ' '.join(suggestions[:2])


def generate_pdf_report(user, logs: list, start: datetime, end: datetime) -> str:
    """
    Generate a professional weekly nutrition PDF report using ReportLab.
    Returns the file path to the generated PDF.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError:
        # Fallback: return a simple text file if ReportLab not installed
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w')
        tmp.write(f'NutriSnap-X Weekly Report\nUser: {user.full_name}\n')
        tmp.write(f'Period: {start.strftime("%Y-%m-%d")} to {end.strftime("%Y-%m-%d")}\n\n')
        for log in logs:
            tmp.write(f'{log.food_name}: {log.calories} kcal\n')
        tmp.close()
        return tmp.name

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    tmp_file.close()

    doc = SimpleDocTemplate(
        tmp_file.name,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title', parent=styles['Title'],
        fontSize=24, textColor=colors.HexColor('#2ECC71'),
        spaceAfter=6, alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=11, textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER, spaceAfter=20
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Heading2'],
        fontSize=14, textColor=colors.HexColor('#2C3E50'),
        spaceBefore=16, spaceAfter=8
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#333333'),
        spaceAfter=4
    )

    elements = []

    # Header
    elements.append(Paragraph('🥗 NutriSnap-X', title_style))
    elements.append(Paragraph('Weekly Nutrition Report', subtitle_style))
    elements.append(Paragraph(
        f'<b>Name:</b> {user.full_name} &nbsp;&nbsp;|&nbsp;&nbsp; '
        f'<b>Period:</b> {start.strftime("%d %b")} – {end.strftime("%d %b %Y")}',
        subtitle_style
    ))
    elements.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#2ECC71')))
    elements.append(Spacer(1, 12))

    # Summary stats
    total_cal  = sum(l.calories for l in logs)
    total_pro  = sum(l.protein  for l in logs)
    total_carb = sum(l.carbs    for l in logs)
    total_fat  = sum(l.fat      for l in logs)
    count      = len(logs) or 1

    elements.append(Paragraph('Weekly Summary', section_style))
    summary_data = [
        ['Metric', 'Total (7 days)', 'Daily Average'],
        ['Calories (kcal)', f'{total_cal:.0f}', f'{total_cal/7:.0f}'],
        ['Protein (g)',     f'{total_pro:.1f}',  f'{total_pro/7:.1f}'],
        ['Carbs (g)',       f'{total_carb:.1f}', f'{total_carb/7:.1f}'],
        ['Fat (g)',         f'{total_fat:.1f}',  f'{total_fat/7:.1f}'],
        ['Foods Logged',   f'{count}',           f'{count/7:.1f}'],
    ]

    summary_table = Table(summary_data, colWidths=[6*cm, 5*cm, 5*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2ECC71')),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,0), 11),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FFF9')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.HexColor('#F8FFF9'), colors.HexColor('#FFFFFF')]),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor('#DDDDDD')),
        ('FONTNAME',   (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',   (0,1), (-1,-1), 10),
        ('ALIGN',      (1,0), (-1,-1), 'CENTER'),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 16))

    # Food log table
    elements.append(Paragraph('Food Log Details', section_style))
    log_data = [['Date & Time', 'Food Item', 'Cal', 'Prot(g)', 'Carbs(g)', 'Source']]

    for log in logs[:30]:  # Limit to 30 rows
        log_data.append([
            log.logged_at.strftime('%d %b %H:%M'),
            log.food_name[:30],
            f'{log.calories:.0f}',
            f'{log.protein:.1f}',
            f'{log.carbs:.1f}',
            log.source.capitalize()
        ])

    log_table = Table(log_data, colWidths=[3.5*cm, 5.5*cm, 2*cm, 2.2*cm, 2.3*cm, 2*cm])
    log_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS',(0,1), (-1,-1),
         [colors.HexColor('#F9F9F9'), colors.white]),
        ('GRID',          (0,0), (-1,-1), 0.3, colors.HexColor('#CCCCCC')),
        ('ALIGN',         (2,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(log_table)

    # Footer
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CCCCCC')))
    elements.append(Paragraph(
        f'Generated by NutriSnap-X on {datetime.now().strftime("%d %B %Y at %H:%M")} '
        f'| Goal: {user.daily_calorie_goal} kcal/day',
        ParagraphStyle('Footer', parent=body_style, fontSize=8,
                       textColor=colors.HexColor('#999999'), alignment=TA_CENTER)
    ))

    doc.build(elements)
    return tmp_file.name
