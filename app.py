from flask import Flask, request, jsonify, redirect, url_for
from extensions import db, login_manager
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# -----------------------------
# App Factory
# -----------------------------
def create_app():
    app = Flask(__name__)

    # Config
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutrisnapx.db'

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    # Register blueprint
    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    # -----------------------------
    # Home Route
    # -----------------------------
    @app.route("/")
    def home():
        return redirect("/login")   # safest (no url_for issues)

    # -----------------------------
    # Chat Page Route
    # -----------------------------
    @app.route("/chat")
    def chat():
        return "NutriGenie Chat Running"

    # -----------------------------
    # Chat API Route
    # -----------------------------
    @auth_bp.route("/api/chat", methods=["POST"])
    def api_chat():
        if not app.client:
            return jsonify({"reply": "⚠️ AI service not configured."})

        data = request.get_json()
        user_msg = data.get("message", "")

        try:
            resp = app.client.chat.completions.create(
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
            print("Chatbot error:", e)
            return jsonify({"reply": "⚠️ AI is temporarily unavailable."})

    return app


# -----------------------------
# Create App
# -----------------------------
app = create_app()

# -----------------------------
# NutriGenie AI Setup
# -----------------------------
openai_key = os.getenv("OPENAI_API_KEY")

if openai_key:
    app.client = OpenAI(api_key=openai_key)
else:
    app.client = None

SYSTEM_PROMPT = """
You are NutriGenie AI — the intelligent assistant inside NutriSnap-X.
You help users with:
- food and nutrition questions
- diet and calorie doubts
- app usage help
- general knowledge questions

Answer clearly and simply.
Avoid medical diagnosis claims.
Keep answers practical.
"""

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)