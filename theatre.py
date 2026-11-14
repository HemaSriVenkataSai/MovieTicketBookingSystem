from flask import Blueprint, jsonify
from config import get_db_connection

theatre_bp = Blueprint("theatre", __name__)


@theatre_bp.route("/theatres", methods=["GET"])
def get_theatres():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM theatres")

    theatres = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(theatres)


@theatre_bp.route("/shows/<int:theatre_id>", methods=["GET"])
def get_shows(theatre_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM shows
        WHERE theatre_id=%s
        """,
        (theatre_id,)
    )

    shows = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(shows)