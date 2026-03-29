from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = "mongodb+srv://evadmin:1234@cluster0.qbwzyfg.mongodb.net/?appName=Cluster0"
DB_NAME = "ev_db"
COLLECTION_NAME = "vehicles"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
base_collection = db[COLLECTION_NAME]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "works"}), 200

@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    data = request.get_json()
    fast_collection = base_collection.with_options(
        write_concern=WriteConcern(w=1)
    )
    result = fast_collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 200

@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    data = request.get_json()

    safe_collection = base_collection.with_options(
        write_concern=WriteConcern("majority")
    )

    result = safe_collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 200

@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
    primary_collection = base_collection.with_options(
        read_preference=ReadPreference.PRIMARY
    )

    count = primary_collection.count_documents({"Make": "TESLA"})
    return jsonify({"count": count}), 200

@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    secondary_collection = base_collection.with_options(
        read_preference=ReadPreference.SECONDARY_PREFERRED
    )

    count = secondary_collection.count_documents({"Make": "BMW"})
    return jsonify({"count": count}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)