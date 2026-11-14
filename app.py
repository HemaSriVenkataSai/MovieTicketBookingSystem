from flask import Flask
from flask_cors import CORS

from routes.user import user_bp
from routes.movie import movie_bp
from routes.theatre import theatre_bp
from routes.booking import booking_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(user_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(theatre_bp)
app.register_blueprint(booking_bp)


@app.route("/")
def home():
    return {
        "message": "Movie Ticket Booking System API Running Successfully"
    }


if __name__ == "__main__":
    app.run(debug=True)