from ..db.connection import db, index
import requests
import time
import os
import csv
from dotenv import load_dotenv
import sys
from pymongo import errors
from ..models.user import UserData
from pydantic import ValidationError
import sys


load_dotenv()
my_collection = db["users"]
top_players_collection = db["top_players"]

api_key = os.getenv("RIVAL_API_KEY")

headers = {
    "x-api-key": api_key
}

def compute_top_player_avg():
    """
    Compute the average win rate of the top players in the database.

    Returns:
        float: The average win rate of the top players.
    """
    hero_accuracy = {}
    categories = ["wins", "kills", "deaths", "assists", "matches"]
    cursor = top_players_collection.find()

    for player in cursor:
        print("Processing player:", player.get("name"))
        hero_stats = player.get("heroes_ranked", {})
        for hero in hero_stats:
            matches = hero.get("matches")
            main_attack = hero.get("main_attack")
            hero_name = hero.get("hero_name")
            if matches is not None and main_attack is not None and hero_name:
                if hero_name not in hero_accuracy:
                    hero_accuracy[hero_name] = {
                        "wins": 0, "matches": 0, 
                        "total_hits": 0, "total_attempts": 0,
                        "kills": 0, "deaths": 0, "assists": 0
                    }

                # Accumulate main_attack stats
                hero_accuracy[hero_name]["total_hits"] += main_attack.get("hits", 0)
                hero_accuracy[hero_name]["total_attempts"] += main_attack.get("total", 0)

                # Accumulate other categories
                for category in categories:
                    hero_accuracy[hero_name][category] += hero.get(category, 0)


    for hero in hero_accuracy:
        total_hits = hero_accuracy[hero]["total_hits"] 
        total_attempts = hero_accuracy[hero]["total_attempts"]
        if total_attempts > 0:
            hero_accuracy[hero]["accuracy"] = total_hits / total_attempts
        else:
            hero_accuracy[hero]["accuracy"] = 0.0

    print("Computed hero accuracies:", hero_accuracy)
    return hero_accuracy

def update_leaders(insert=False):
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

    with open('../data/s5_leaderboard_meta.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (top_players_collection.find_one({"name": row['Name']})):
                print(f"User {row['Name']} already exists in the database. Skipping insertion.")
                continue
            users.append(row['Rivals_uid'])
            
            
    for i in range(75):
        user_id = users[i]
        status = 0
        txt = "mt"
        if insert:
                __, status = fetch_user(user_id, top_players=True)
        else:
            response = update_user(user_id)
            status = response.status_code
            txt = response.text

        if status == 200:
            print(f"Successfully updated/inserted user {user_id}")
        elif insert == False:
            print(f"Failed to update user {user_id}: {status}, reponse text: {txt}")
        else:
            print(f"Failed to insert user {user_id}: {status}")
        time.sleep(10)

    return {"users": users}

def fetch_user(user_id: str, top_players=False):
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
            return "error: Data validation failed", 500

        
        try: 
            if (top_players):
                top_players_collection.insert_one(user.dict())
            else:
                my_collection.insert_one(user.dict())

        except errors.OperationFailure:
            print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
            sys.exit(1)

        return user, 200
    elif response.status_code == 404:
        return "error: response.text", 404
    elif response.status_code == 403:
        return "error: response.text", 403

    return "error: User stats could not be retrieved", 404


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
        - Updates user data through an external API.
    """

    url = f"https://marvelrivalsapi.com/api/v1/player/{user_id}/update"

    response = requests.get(url, headers=headers)

    print("Status code for updating:", response.status_code)

    if response.status_code == 404:
        print("User not found: ", user_id)
    elif response.status_code == 403:
        print("User profile is private: ", user_id)
    
    return response



def hero_leader_averages():
    """
    Retrieve the average statistics for a specific hero among top players.

    Args:
        name (str): The name of the hero.
    """

    results = index.search(
        namespace="__default__", 
        query={
                "inputs": {"text": "strategist"}, 
                "top_k": 45
        },
        fields=["category", "chunk_text"]
    )
    

    url = "https://marvelrivalsapi.com/api/v1/heroes/leaderboard/"

    fields = [
            "name",
            "role",
            "matches",
            "wins",
            "kills",
            "deaths",
            "assists",
            "play_time",
            "total_hero_damage",
            "total_damage_taken",
            "total_hero_heal",
            "mvps",
            "svps"
    ]

    with open(f'../data/hero_leaderboard.csv', 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fields)

      writer.writeheader()

      for record in results['result']['hits']:
        name = str(record['fields']['category'][0].split(":")[1].strip())
        role = str(record['fields']['category'][1].split(":")[1].strip())

        hero_url = url + name
        response = requests.get(hero_url, headers=headers)

        totals = {
            "name": name,
            "role": role,
            "matches": 0,
            "wins": 0,
            "kills": 0,
            "deaths": 0,
            "assists": 0,
            "play_time": 0,
            "total_hero_damage": 0,
            "total_damage_taken": 0,
            "total_hero_heal": 0,
            "mvps": 0,
            "svps": 0
        }

        print("Status code for updating:", response.status_code)
        data = response.json()  # Parse JSON response
        for entry in data["players"][:20]:
            for key in totals.keys():
                if key == "name" or key == "role":
                    continue
                first = key.split("_")[0]
                if first == "total" or first == "play":
                    totals[key] += float(entry[key])
                else:
                    totals[key] += entry[key]

        writer.writerow(totals)


if __name__ == "__main__":
    # update_leaders(insert=True)
    # compute_top_player_avg()
    hero_leader_averages()