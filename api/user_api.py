from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

from database.connection import cnxn

api_bp = Blueprint('User', __name__, url_prefix="/api/User")


@api_bp.route("/", methods=["PUT"])
def update_user():
    try:
        json_data = request.json
        user_id = json_data["UserId"]
        user_name = json_data['UserName']
        email = json_data['Email']

        curses = cnxn.cursor()
        curses.execute(f"SELECT * FROM Users WHERE UserId={user_id}")
        row = curses.fetchone()

        if not row:
            return jsonify({"error": "Id'ye ait değer bulunamadı!"}), 400

        cursor = cnxn.cursor()
        cursor.execute(f"UPDATE Users SET Username = '{user_name}', Email = '{email}' WHERE UserId={user_id}")
        cnxn.commit()

        return jsonify(json_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    try:
        cursor = cnxn.cursor()
        cursor.execute(f"DELETE FROM Users WHERE UserId={user_id};")
        cnxn.commit()
        return "Veri başarıyla silindi!", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/", methods=['POST'])
def add_user():
    try:
        json_data = request.json

        user_name = json_data['UserName']
        email = json_data['Email']

        cursor = cnxn.cursor()
        cursor.execute(f"INSERT INTO Users (UserName, Email) VALUES ('{user_name}', '{email}')")
        cnxn.commit()

        return jsonify(json_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@jwt_required()
@api_bp.route('/getAll')
def get_all_users():
    try:
        current_user = verify_jwt_in_request()

        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM Users")
        rows = cursor.fetchall()

        users = []
        for row in rows:
            user = {
                "UserId": row.UserId,
                "Username": row.Username,
                "Email": row.Email
            }
            users.append(user)

        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/<user_id>")
def get_user_from_id(user_id):
    try:
        curses = cnxn.cursor()
        curses.execute(f"SELECT * FROM Users WHERE UserId={user_id}")
        row = curses.fetchone()
        if row:
            return jsonify({
                "UserId": row.UserId,
                "Username": row.Username,
                "Email": row.Email
            })
        return jsonify({"message": "Id'ye ait kullanıcı bulunamadı!"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400
