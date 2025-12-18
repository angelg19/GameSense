from flask import Blueprint, jsonify
import requests
from dotenv import load_dotenv
import os
from db.connection import db, index
import sys
from pymongo import errors
from models.user import UserData
import csv
import time
from pydantic import ValidationError
from services.user_data_format import cleanup_user_data
from datetime import datetime

load_dotenv()

# Access variables
api_key = os.getenv("RIVAL_API_KEY")
my_collection = db["users"]
top_players_collection = db["top_players"]

headers = {
    "x-api-key": api_key
}


users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_users():
    result = my_collection.find()
    if result:    
        for doc in result:
            for key, value in doc.items():
                print(f"{key}: {value}")
    else:
        print("No documents found.")
    return jsonify({"users": ["Alice", "Bob", "Charlie"]})



@users_bp.route("/updateLeaders", methods=["GET"])
def update_leaders():
    """
    Updates the information on the top 1000 players such as match performances, heroes played, 
    hero matchups, and more in the database.

    Returns:
        tuple: A tuple containing:
            - dict: The user's data (cleaned up).
            - int: HTTP status code (200 for success, or the status code from fetch_user).
    
    Behavior:
        - Retrieves the names of the top 1000 players in the leaderboard from a csv file.
        - Iterates through each name and checks if the user already has their information updated in the db.
        - If found, skip.
        - If not found, fetches user data from an external source using `fetch_user`.
    """
    
    users = []

    with open('../data/leaderboard_wr.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (top_players_collection.find_one({"name": row['Name']})):
                print(f"User {row['Name']} already exists in the database. Skipping insertion.")
                continue
            users.append(row['Name'])
            
            
    for i in range(len(users)):
        user_id = users[i]

        __, status = fetch_user(user_id, top_players=True)
        if status == 200:
            print(f"Successfully retrieved user {user_id}")
            
        else:
            print(f"Failed to update user {user_id}: {status}")
        time.sleep(2)

    return jsonify({"users": users})



@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id: str):
    """
    Retrieve user information from the database or fetch it externally if not found.

    Args:
        user_id (str): The unique identifier or username of the user.

    Returns:
        tuple: A tuple containing:
            - dict: The user's data (cleaned up).
            - int: HTTP status code (200 for success, or the status code from fetch_user).
    
    Behavior:
        - Checks if the user exists in the local database (MongoDB).
        - If found, removes the internal '_id' field and returns cleaned data.
        - If not found, fetches user data from a helper function called `fetch_user`.
    """
    existing_user = my_collection.find_one({"name": user_id})
    if not existing_user:
        try:
            num = int(user_id)
            existing_user = my_collection.find_one({"rivals_uid": num})
        except ValueError:
            pass
    

    if existing_user:

        if existing_user.pop('is_refresh', False):
            updated_user, status = fetch_user(user_id=user_id, top_players=False, insert=False)
            if status != 200:
                print("Something went wrong with retrieving stats after updating: ", status)
                return updated_user, status
            print("Successfully updated")
            ins = updated_user.dict()
            ins['is_refresh'] = False
            my_collection.update_one(
                {"name": user_id},
                {"$set": ins}
            )

            ret_data = cleanup_user_data(UserData(**ins))
            return ret_data, 200


        print(f"User {user_id} already exists in the database. Retrieved info.")
        existing_user.pop("_id", None)
        existing_user.pop("last_update", None)
        ret_data = cleanup_user_data(UserData(**existing_user))
        return ret_data, 200

    data, status = fetch_user(user_id)

    # Check status
    if status == 200:
        ret_data = cleanup_user_data(data)
        return ret_data, 200
    else:
        #response = update_user(user_id)
        # if response.status_code != 200:
        #     print(response)
        return data, status



def fetch_user(user_id: str, top_players=False, insert=True):
    """
    Retrieve user information from the database or fetch it externally if not found.

    Args:
        user_id (str): The unique identifier or username of the user.

    Returns:
        tuple: A tuple containing:
            - dict: The user's data (cleaned up).
            - int: HTTP status code (200 for success, or the status code from fetch_user).
    
    Behavior:
        - Checks if the user exists in the local database (MongoDB).
        - If found, removes the internal '_id' field and returns cleaned data.
        - If not found, fetches user data from an external source using `fetch_user`.
    """

    url = f"https://marvelrivalsapi.com/api/v1/player/{user_id}"

    response = requests.get(url, headers=headers)

    print("Status code:", response.status_code)
    
    # Check status
    if response.status_code == 200:
        fields_keep = ["player", "heroes_ranked", "maps", "overall_stats"]
        if not top_players:
            fields_keep.append("matchups")
        data = response.json()  # Parse JSON response

        filtered_data = {key: data[key] for key in fields_keep if key in data}
        filtered_data["name"] = data["player"]["name"]
        filtered_data["rivals_uid"] = data["player"]["uid"]
        try:
            user = UserData(**filtered_data)
        except ValidationError as e:
            print("Validation error:", e)
            return jsonify({"error": "Data validation failed"}), 500

        
        try: 
            if top_players and insert:
                top_players_collection.insert_one(user.dict())
            elif insert:
                my_collection.insert_one(user.dict())

        except errors.OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
            sys.exit(1)

        return user, 200
    elif response.status_code == 404:
        return jsonify({"error": response.text}), 404
    elif response.status_code == 403:
        return jsonify({"error": response.text}), 403

    return jsonify({"error": "User stats could not be retrieved"}), 404



@users_bp.route("/<user_id>/refresh", methods=["POST"])
def update_user(user_id: str):
    """
    Refresh the users profile so the latest stats can be retrieved from the API.

    Args:
        user_id (str): The unique identifier or username of the user.

    Returns:
        tuple: A tuple containing:
            - dict: The user's data (cleaned up).
            - int: HTTP status code (200 for success, or the status code from fetch_user).
    
    Behavior:
        - Checks if the user exists in the local database (MongoDB).
        - If found, removes the internal '_id' field and returns cleaned data.
        - If not found, fetches user data from an external source using `fetch_user`.
    """

    url = f"https://marvelrivalsapi.com/api/v1/player/{user_id}/update"

    existing_user = my_collection.find_one({"name": user_id})
    
    if not existing_user:
        return jsonify({"error": "Your profile is not in the database yet and thus can't be updated."}), 404

    response = requests.get(url, headers=headers)

    print("Status code for updating:", response.status_code)

    # Check status
    if response.status_code == 200:

        now = datetime.now()
        new_values = {"last_update": now, "is_refresh": True}
        my_collection.update_one(
            {"name": user_id},
            {"$set": new_values}
        )
        return jsonify({"Success": "User is being updated"}), 200
    
    elif response.status_code == 404:
        return jsonify({"error": "User not found"}), 404
    elif response.status_code == 403:
        return jsonify({"error": "User profile is private"}), 403

    return jsonify({"Success": "User is being updated"}), 200
