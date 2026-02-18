from flask import Flask
from extensions import db, login_manager
@app.route("/chat")
def chat_page():
    return render_template("chat.html")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'nutrisnapx-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutrisnapx.db'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app


app = create_app()

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

