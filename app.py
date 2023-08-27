from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from api.auth_api import api_auth
from api.user_api import api_bp
from database.connection import cnxn

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'deneme_apim_icin_jwt_secret_key'  # Gerektiğinde değiştirin
jwt = JWTManager(app)

# Blueprint'i kaydetme
app.register_blueprint(api_bp)
app.register_blueprint(api_auth)


def create_app():
    return app
