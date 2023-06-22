from os import getenv
from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
from models.openai import OpenAI
from flask_caching import Cache

app = Flask(__name__)
CORS(app)

app.config["CACHE_TYPE"] = "simple"
cache = Cache(app)

openai_api = OpenAI(
    organization=getenv("ORGANIZATION"),
    api_key=getenv("API_KEY"),
    model="text-davinci-003"
)


@app.before_request
def middleware():
    if request.method != "OPTIONS":
        authorization = request.headers.get("Authorization")
        if not authorization or authorization.split(" ")[1] != getenv("SECRET"):
            return make_response({"message": "Unauthorized"}), 401


@app.route("/api/ask-me", methods=["POST"])
def ask():
    question = request.json.get("question")
    if not question or len(question) == 0:
        return make_response(jsonify({
            "status": 400,
            "message": "Question must not be empty"
        })), 400

    response = cache.get(question)

    if not response:
        response = openai_api.create_response(question)
        cache.set(question, response, timeout=60*5)

    return make_response(jsonify({
        "status": 200,
        "question": question,
        "response": response
    })), 200
    
@app.route("/api/clear-cache", methods=["GET"])
def clear_cache():
    cleared = cache.clear()
    if cleared:
        openai_api.clear_history()
        return make_response(jsonify({
            "status": 200,
            "message": "Cache has been cleared successfully",
        })), 200
    return make_response(jsonify({
        "status": 400,
        "message": "Fail in clear cache",
    })), 200
    