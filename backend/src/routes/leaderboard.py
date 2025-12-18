from flask import Blueprint, jsonify
import requests
from dotenv import load_dotenv
import os
from db.connection import db, index
import csv

load_dotenv()

# Access variables
api_key = os.getenv("RIVAL_API_KEY")
my_collection = db["users"]
top_players_collection = db["top_players"]

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.route("/", methods=["GET"])
def get_leaderboard():
    with open('../data/hero_leaderboard.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    for row in rows:
        row["win_rate"] = round(int(row["wins"]) / int(row["matches"]), 2) if int(row["matches"]) > 0 else 0.0
        row["mvp_rate"] = round(int(row["mvps"]) / int(row["matches"]), 2) if int(row["matches"]) > 0 else 0.0
        row["svp_rate"] = round(int(row["svps"]) / int(row["matches"]), 2) if int(row["matches"]) > 0 else 0.0
        row["kpg"] = round(int(row["kills"]) / int(row["matches"]), 2) if int(row["matches"]) > 0 else 0.0
        row['dpg'] = round(int(row["deaths"]) / int(row["matches"]), 2) if int(row["matches"]) > 0 else 0.0
        row['apg'] = round(int(row["assists"]) / int(row["matches"]), 2) if int(row["matches"]) > 0 else 0.0


    return jsonify({"leaderboard": rows})