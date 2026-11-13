
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Allow requests from Express frontend
CORS(app, origins=["http://localhost:3000"])

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

db = client["my_test_database"]
collection = db["Students"]

@app.route("/", methods=["GET"])
def home():
    return "Flask Backend is Running!"


@app.route("/submit", methods=["POST"])
def submit():

    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")

        if not name or not email or not phone:
            return jsonify({
                "error": "All fields are required"
            }), 400

        student = {
            "name": name,
            "email": email,
            "phone": phone
        }

        collection.insert_one(student)

        return jsonify({
            "message": "Data submitted successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
