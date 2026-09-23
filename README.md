# 🥗 NutriSnap-X (Claude)
### AI-Based Food Nutrition Analysis Web Application
**B.Tech Major Project | Full-Stack Flask Application**

---

## 🚀 Quick Start

```bash
# 1. Clone or extract the project
cd NutriSnap-X

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (optional)
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY if desired

# 5. Run the app
python app.py
```

Open your browser at **http://localhost:5000**

---

## 📁 Project Structure

```
NutriSnap-X/
│
├── app.py                  ← Main Flask app (entry point)
├── extensions.py           ← SQLAlchemy + LoginManager init
├── requirements.txt        ← Python dependencies
├── Procfile                ← Render / Heroku deployment
├── .env.example            ← Environment variable template
├── .gitignore
├── README.md
│
├── auth/
│   ├── __init__.py
│   └── routes.py           ← Register, Login, Logout blueprint
│
├── database/
│   ├── __init__.py
│   └── models.py           ← User, FoodLog, BarcodeLog models
│
├── nutrition/
│   ├── __init__.py
│   └── nutrition_db.py     ← Local nutrition reference database
│
├── utils/
│   ├── __init__.py
│   └── helpers.py          ← Health score, PDF report, mock AI detection
│
├── templates/
│   ├── base.html           ← Base layout with sidebar + topbar
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html      ← Main dashboard
│   ├── analyze.html        ← Food image upload
│   ├── analyze_result.html ← Detection result
│   ├── barcode.html        ← Barcode scanner
│   ├── analytics.html      ← Charts
│   ├── logs.html           ← Food diary
│   ├── report.html         ← PDF download page
│   ├── chat.html           ← AI chatbot
│   └── profile.html        ← User settings
│
├── static/
│   ├── css/
│   │   └── style.css       ← Full custom stylesheet
│   ├── js/
│   │   ├── theme.js        ← Light/Dark/System theme engine
│   │   └── app.js          ← Sidebar, animations, utilities
│   └── uploads/            ← User-uploaded food images
│
└── instance/
    └── nutrisnap.db        ← SQLite database (auto-created)
```

---

## ✨ Features

| Feature | Details |
|---|---|
| **Authentication** | Register, Login, Logout with password hashing |
| **Dashboard** | Calories, macros, health score, weekly avg, tips |
| **Food Image Analysis** | Upload → AI detection → Nutrition → Auto-logged |
| **Barcode Scanner** | Camera scan via html5-qrcode → OpenFoodFacts API |
| **AI Fallback** | Rule-based estimation when product not found |
| **Manual Entry** | Quick form to log nutrition manually |
| **Analytics** | 7/14/30-day calorie, protein, carbs charts |
| **PDF Report** | Professional weekly nutrition summary |
| **AI Chatbot** | OpenAI GPT-3.5 or rule-based fallback |
| **Theme System** | Light / Dark / System — saved in localStorage |
| **Responsive UI** | Mobile + tablet + desktop layouts |

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3.0, Blueprint pattern |
| Database | SQLite via SQLAlchemy ORM |
| Auth | Flask-Login + Werkzeug password hashing |
| Frontend | Bootstrap 5, Vanilla JS |
| Charts | Chart.js 4 |
| Barcode | html5-qrcode library |
| Nutrition API | OpenFoodFacts (free, no key needed) |
| AI Chat | OpenAI GPT-3.5 (optional) / rule-based fallback |
| PDF | ReportLab |
| Fonts | Syne + DM Sans (Google Fonts) |
| Deployment | Gunicorn + Render / Railway / Heroku |

---

## ⚙️ Configuration

All configuration is done via environment variables in `.env`:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | auto | Flask secret — change in production |
| `OPENAI_API_KEY` | (empty) | Enables real AI chatbot |
| `FLASK_DEBUG` | `true` | Set to `false` in production |
| `PORT` | `5000` | Server port |

The app works fully **without** an OpenAI key — the chatbot falls back to an intelligent rule-based system.

---

## ☁️ Deployment (Render)

1. Push your project to a GitHub repository
2. Create a new **Web Service** on [render.com](https://render.com)
3. Connect your GitHub repo
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add environment variables in the Render dashboard
6. Deploy 🚀

---

## 📊 API Endpoints

| Method | Route | Description |
|---|---|---|
| POST | `/api/barcode/lookup` | Lookup barcode via OpenFoodFacts |
| POST | `/api/barcode/manual` | Log food manually |
| GET  | `/api/analytics/data` | Chart data (days param) |
| GET  | `/api/report/generate` | Download PDF report |
| POST | `/api/chat` | AI nutrition chatbot |
| DELETE | `/api/log/delete/<id>` | Delete a food log entry |

---

## 🎓 For Viva

- **Architecture:** MVC-style Flask Blueprint pattern with separation of concerns
- **Database:** SQLAlchemy ORM with proper relationship modeling and absolute SQLite path
- **Security:** Password hashing (Werkzeug PBKDF2), login required decorators, CSRF via Flask session
- **AI Integration:** Mock food detection + OpenFoodFacts API + OpenAI GPT-3.5 (with graceful fallback)
- **Scalability:** Blueprint architecture supports adding new modules without touching core app
- **Deployment:** Production-ready with Gunicorn WSGI server and environment variable configuration

---

## 📝 License

Built for educational purposes as a B.Tech Major Project.

---

*Made with ❤️ using Flask + Bootstrap 5 + Chart.js*
