from os import getenv
from flask import Flask, make_response, request
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.before_request
def middleware():
    
    authorization = request.headers.get("Authorization").split(" ")[1] if request.headers.get("Authorization") else None

    if request.method != "OPTIONS" and not authorization == getenv("SECRET"):
        return make_response({"message": "Unauthorized"}), 401

@app.route("/api/ask-me", methods=["POST"])
def ask():

    question = request.json["question"] if request.json["question"] else None
    openai.organization = getenv("ORGANIZATION") if getenv("ORGANIZATION") else None
    openai.api_key = getenv("API_KEY") if getenv("API_KEY") else None

    if question == None or len(question) == 0:
        return make_response({
        "status": 400,
        "message": "question must be not empty"
    }), 400
        
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0,
        max_tokens=2000
    )

    return make_response({
        "status": 200,
        "question": question,
        "response": response.choices[0].text
    }), 200
    
   

