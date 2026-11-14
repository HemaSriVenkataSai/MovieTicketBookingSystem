# -------------------------------
# Admin - View All Users
# -------------------------------
@user_bp.route("/admin/users", methods=["GET"])
def get_all_users():

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            user_id,
            name,
            email,
            phone
        FROM users
        ORDER BY user_id DESC
    """)

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(users)