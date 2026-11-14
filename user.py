from flask import Blueprint, request
from config import get_db_connection

user_bp = Blueprint("user", __name__)


# ---------------- REGISTER ---------------- #

@user_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data["name"]
    email = data["email"]
    password = data["password"]
    phone = data["phone"]

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO users(name, email, password, phone)
    VALUES(%s, %s, %s, %s)
    """

    cursor.execute(query, (name, email, password, phone))

    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "User Registered Successfully"}


# ---------------- LOGIN ---------------- #

@user_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data["email"]
    password = data["password"]

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT * FROM users
    WHERE email=%s AND password=%s
    """

    cursor.execute(query, (email, password))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        return {"message": "Login Successful"}
    else:
        return {"message": "Invalid Email or Password"}