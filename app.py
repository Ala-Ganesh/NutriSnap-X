from flask import Flask, redirect
from extensions import db, login_manager
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

    # Home Route
    @app.route("/")
    def home():
        return redirect("/login")

    return app   # ✅ VERY IMPORTANT

# Create app instance
app = create_app()

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)