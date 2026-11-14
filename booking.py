from flask import Blueprint, request, jsonify
from config import get_db_connection
from datetime import date

booking_bp = Blueprint("booking", __name__)


# -------------------------------
# Book Ticket
# -------------------------------
@booking_bp.route("/book-ticket", methods=["POST"])
def book_ticket():

    data = request.get_json()

    user_email = data.get("user_email")
    movie_title = data.get("movie_title")
    theatre_name = data.get("theatre_name")
    show_time = data.get("show_time")
    seats = data.get("seats")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT seats
        FROM bookings
        WHERE movie_title=%s
        AND theatre_name=%s
        AND show_time=%s
    """, (
        movie_title,
        theatre_name,
        show_time
    ))

    booked_rows = cursor.fetchall()

    booked_seats = set()

    for row in booked_rows:
        for seat in row["seats"].split(","):
            booked_seats.add(seat.strip())

    selected_seats = [seat.strip() for seat in seats.split(",")]

    already_booked = []

    for seat in selected_seats:
        if seat in booked_seats:
            already_booked.append(seat)

    if already_booked:

        cursor.close()
        conn.close()

        return jsonify({
            "message":
            "Seat(s) already booked: " +
            ", ".join(already_booked)
        }), 400

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings
        (user_email,movie_title,theatre_name,show_time,seats,booking_date)
        VALUES(%s,%s,%s,%s,%s,%s)
    """, (
        user_email,
        movie_title,
        theatre_name,
        show_time,
        seats,
        date.today()
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message":"Ticket Booked Successfully"})


# -------------------------------
# User Bookings
# -------------------------------
@booking_bp.route("/bookings/<email>", methods=["GET"])
def get_bookings(email):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM bookings
        WHERE user_email=%s
        ORDER BY booking_id DESC
    """,(email,))

    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(bookings)


# -------------------------------
# Admin View All Bookings
# -------------------------------
@booking_bp.route("/admin/bookings", methods=["GET"])
def admin_bookings():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM bookings
        ORDER BY booking_id DESC
    """)

    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(bookings)


# -------------------------------
# User Cancel Booking
# -------------------------------
@booking_bp.route("/cancel-booking/<int:booking_id>", methods=["DELETE"])
def cancel_booking(booking_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bookings WHERE booking_id=%s",
        (booking_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message":"Booking Cancelled Successfully"
    })


# -------------------------------
# Admin Delete Booking
# -------------------------------
@booking_bp.route("/admin/delete-booking/<int:booking_id>", methods=["DELETE"])
def admin_delete_booking(booking_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bookings WHERE booking_id=%s",
        (booking_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message":"Booking Deleted Successfully"
    })