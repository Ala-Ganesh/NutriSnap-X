# 🥗 NutriSnap-X — AI Nutrition Intelligence System

NutriSnap-X is a full-stack AI-powered web application that detects food from images and provides detailed nutritional analysis, health insights, and personalized recommendations.

This project is developed as a **B.Tech Major Project** integrating **Computer Vision, Machine Learning, and Web Development** into a deployable system.

---

## 🚀 Key Features

### 🤖 AI Food Detection
- Detects food items from uploaded images
- Uses pretrained **Food-101 deep learning model**
- Displays predicted food with nutritional values

### 📊 Nutrition Analysis
- Calories, Protein, Carbohydrates estimation
- Health Score (0–100) per meal
- Smart dietary insights

### 🎯 Goal-Based System
Users can select goals:
- Weight Loss
- Weight Gain
- Gym / Muscle Building
- Standard Healthy Diet
- Senior Citizen

System adjusts recommendations dynamically.

### 📈 Weekly Analytics Dashboard
- Weekly calorie tracking
- Protein & carb monitoring
- Average daily intake
- Limit-based alerts

### 🧠 Smart Alerts Engine
- Overeating detection
- Low protein warnings
- Health score analysis

### 🤝 Personalization Engine
- AI-generated diet suggestions
- Goal-based recommendations
- Weekly performance feedback

### 📄 PDF Report Generation
- Weekly AI Nutrition Report
- Includes:
  - User data
  - Metrics
  - Health score
  - Personalized advice
- Professionally formatted using ReportLab

### 📷 Barcode Scanner
- Scan packaged foods
- Fetch nutrition instantly

### 🔐 Authentication System
- User registration & login
- Secure password hashing
- Session management

### 🔒 Privacy & Data Policy
- Transparent data handling
- Academic prototype security standards

---

## 🧠 Technologies Used

| Category | Technologies |
|--------|-------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Bootstrap |
| Database | SQLite, SQLAlchemy |
| AI/ML | PyTorch, Food-101 |
| Image Processing | OpenCV, Pillow |
| Reports | ReportLab |
| Authentication | Flask-Login |
| Deployment | Render |

---

## 🏗️ System Architecture
# 🥗 NutriSnap-X — AI Nutrition Intelligence System

NutriSnap-X is a full-stack AI-powered web application that detects food from images and provides detailed nutritional analysis, health insights, and personalized recommendations.

This project is developed as a **B.Tech Major Project** integrating **Computer Vision, Machine Learning, and Web Development** into a deployable system.

---

## 🚀 Key Features

### 🤖 AI Food Detection
- Detects food items from uploaded images
- Uses pretrained **Food-101 deep learning model**
- Displays predicted food with nutritional values

### 📊 Nutrition Analysis
- Calories, Protein, Carbohydrates estimation
- Health Score (0–100) per meal
- Smart dietary insights

### 🎯 Goal-Based System
Users can select goals:
- Weight Loss
- Weight Gain
- Gym / Muscle Building
- Standard Healthy Diet
- Senior Citizen

System adjusts recommendations dynamically.

### 📈 Weekly Analytics Dashboard
- Weekly calorie tracking
- Protein & carb monitoring
- Average daily intake
- Limit-based alerts

### 🧠 Smart Alerts Engine
- Overeating detection
- Low protein warnings
- Health score analysis

### 🤝 Personalization Engine
- AI-generated diet suggestions
- Goal-based recommendations
- Weekly performance feedback

### 📄 PDF Report Generation
- Weekly AI Nutrition Report
- Includes:
  - User data
  - Metrics
  - Health score
  - Personalized advice
- Professionally formatted using ReportLab

### 📷 Barcode Scanner
- Scan packaged foods
- Fetch nutrition instantly

### 🔐 Authentication System
- User registration & login
- Secure password hashing
- Session management

### 🔒 Privacy & Data Policy
- Transparent data handling
- Academic prototype security standards

---

## 🧠 Technologies Used

| Category | Technologies |
|--------|-------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Bootstrap |
| Database | SQLite, SQLAlchemy |
| AI/ML | PyTorch, Food-101 |
| Image Processing | OpenCV, Pillow |
| Reports | ReportLab |
| Authentication | Flask-Login |
| Deployment | Render |

---

## 🏗️ System Architecture
# 🥗 NutriSnap-X — AI Nutrition Intelligence System

NutriSnap-X is a full-stack AI-powered web application that detects food from images and provides detailed nutritional analysis, health insights, and personalized recommendations.

This project is developed as a **B.Tech Major Project** integrating **Computer Vision, Machine Learning, and Web Development** into a deployable system.

---

## 🚀 Key Features

### 🤖 AI Food Detection
- Detects food items from uploaded images
- Uses pretrained **Food-101 deep learning model**
- Displays predicted food with nutritional values

### 📊 Nutrition Analysis
- Calories, Protein, Carbohydrates estimation
- Health Score (0–100) per meal
- Smart dietary insights

### 🎯 Goal-Based System
Users can select goals:
- Weight Loss
- Weight Gain
- Gym / Muscle Building
- Standard Healthy Diet
- Senior Citizen

System adjusts recommendations dynamically.

### 📈 Weekly Analytics Dashboard
- Weekly calorie tracking
- Protein & carb monitoring
- Average daily intake
- Limit-based alerts

### 🧠 Smart Alerts Engine
- Overeating detection
- Low protein warnings
- Health score analysis

### 🤝 Personalization Engine
- AI-generated diet suggestions
- Goal-based recommendations
- Weekly performance feedback

### 📄 PDF Report Generation
- Weekly AI Nutrition Report
- Includes:
  - User data
  - Metrics
  - Health score
  - Personalized advice
- Professionally formatted using ReportLab

### 📷 Barcode Scanner
- Scan packaged foods
- Fetch nutrition instantly

### 🔐 Authentication System
- User registration & login
- Secure password hashing
- Session management

### 🔒 Privacy & Data Policy
- Transparent data handling
- Academic prototype security standards

---

## 🧠 Technologies Used

| Category | Technologies |
|--------|-------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, Bootstrap |
| Database | SQLite, SQLAlchemy |
| AI/ML | PyTorch, Food-101 |
| Image Processing | OpenCV, Pillow |
| Reports | ReportLab |
| Authentication | Flask-Login |
| Deployment | Render |

---

## 🏗️ System Architecture
NutriSnap-X/
│
├── app.py
├── auth/
├── database/
├── food_detection/
├── nutrition/
├── utils/
├── templates/
├── static/
├── extensions.py
├── requirements.txt
├── Procfile
└── .gitignore


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Ala-Ganesh/NutriSnap-X.git
cd NutriSnap-X

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Application
python app.py

5️⃣ Open in Browser
http://127.0.0.1:5000

☁️ Deployment (Render)

Use gunicorn app:app

Add environment variables if needed

Ensure requirements.txt includes all dependencies

🧠 System Workflow

User uploads food image

AI model detects food item

Nutrition values are estimated

Health score is calculated

Data stored in database

Dashboard & analytics updated

Personalized suggestions generated

🎯 Project Objectives

Automate food tracking using AI

Reduce manual diet logging effort

Provide real-time nutrition insights

Enable personalized health recommendations

🔒 Security Features

Password hashing (Werkzeug)

Session-based authentication

Secure file uploads

📊 Future Enhancements

Real-time camera detection (Google Lens style)

Multi-food detection in one image

Mobile app integration

Cloud database (PostgreSQL)

Advanced AI model fine-tuning

👨‍🎓 Academic Details

Project Type: B.Tech Major Project

Domain: Artificial Intelligence + Web Development

Focus: HealthTech / Nutrition Intelligence

👥 Developed By

Ala Ganesh
B.Tech (CSE - Data Science)

📜 License

This project is developed for academic purposes only.

⭐ Final Note

NutriSnap-X demonstrates how AI can be integrated into everyday life to promote healthier eating habits through intelligent automation.
