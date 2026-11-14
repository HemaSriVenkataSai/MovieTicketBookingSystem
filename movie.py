from flask import Blueprint, request, jsonify
import requests
from config import OMDB_API_KEY

movie_bp = Blueprint("movie", __name__)


@movie_bp.route("/movies", methods=["GET"])
def search_movies():

    movie_name = request.args.get("search")

    if not movie_name:
        return jsonify({
            "message": "Please enter a movie name"
        }), 400

    url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={movie_name}"

    response = requests.get(url)

    data = response.json()

    if data.get("Response") == "False":
        return jsonify({
            "movies": []
        })

    return jsonify(data["Search"])


@movie_bp.route("/movie/<imdb_id>", methods=["GET"])
def get_movie(imdb_id):

    url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"

    response = requests.get(url)

    movie = response.json()

    return jsonify(movie)