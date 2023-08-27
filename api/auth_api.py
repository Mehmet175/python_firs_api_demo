from flask import Flask, jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

from database.connection import cnxn

api_auth = Blueprint('Auth', __name__, url_prefix="/api/Auth")


@api_auth.route('/login/<user_id>', methods=['POST'])
def login(user_id):
    try:
        curses = cnxn.cursor()
        curses.execute(f"SELECT * FROM Users WHERE UserId={user_id}")
        row = curses.fetchone()
        if not row:
            return jsonify({"error": "Id'ye ait kullanıcı bulunamadı!"}), 401

        access_token = create_access_token(identity={
            "UserId": row.UserId
        })
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400