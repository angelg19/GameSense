import requests
from dotenv import load_dotenv
import os
from ..db.connection import db, index
import csv

load_dotenv()

# Access variables
api_key = os.getenv("RIVAL_API_KEY")
my_collection = db["users"]
top_players_collection = db["top_players"]

headers = {
    "x-api-key": api_key
}

def get_maps():
    """
    Grab the most recent data for every competitive map and return it as a structured list.
    """

    url = f"https://marvelrivalsapi.com/api/v1/maps"
    params = {
        "limit":100
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch data from Rivals API")
        return "Failed to fetch data from Rivals API"
    
    data = response.json()
    comp_maps = []
    fields_to_keep = ["id", "game_mode", "name", "location"]
    for map in data["maps"]:
        if (map.get("is_competitive", "")):
            keep = {field: map[field] for field in fields_to_keep if field in map}
            comp_maps.append(keep)
            
    print(comp_maps)
    return comp_maps


def update_heroes_pinecone(name='all'):
    """
    Grab the most recent data for every hero and push it to Pinecone.

    Args:
        name (str): Indicates which Hero should be updated in the pinecone db.
            If name = 'all' then every hero will be updated.

    Returns: 
        JSON response indicating success.

    """
    records = []
    if name != 'all':
        url = f'https://marvelrivalsapi.com/api/v1/heroes/hero/{name}'
        response = requests.get(url, headers=headers)

        print("Status code:", response.status_code)
        data = response.json()  # Parse JSON response
        formatted = format_hero_data(data, 'hero43')
        records.append(formatted)
        
    else:
        url = "https://marvelrivalsapi.com/api/v1/heroes"

        response = requests.get(url, headers=headers)

        print("Status code:", response.status_code)
        data = response.json()  # Parse JSON response

        for i, hero in enumerate(data):
            id = f'hero{i}'
            formatted = format_hero_data(hero, id)
            records.append(formatted)

    index.upsert_records('__default__', records)
    print("Heroes updated in Pinecone successfully.")
    return "Heroes updated in Pinecone successfully."



def format_hero_data(hero, id):
    """
    Format the given hero data for Pinecone insertion.

    Args:
        hero (obj): The hero data from Rivals API.
        id (str): The unique identifier in Pinecone for the hero.

    Returns:
        tuple: A tuple containing:
            - dict: The user's data (cleaned up).
            - int: HTTP status code (200 for success, or the status code from fetch_user).
    
    """

    name = hero.get("name")
    real_name = hero.get("real_name")
    role = hero.get("role")
    attack_type = hero.get("attack_type")
    difficulty = hero.get("difficulty")
    abilities = hero.get("abilities", [])

    ability_texts = []
    for idx, ability in enumerate(abilities, 1):
        # Flatten additional fields
        additional = ability.get("additional_fields", {})
        additional_text = ", ".join(f"{k}: {v}" for k, v in additional.items()) if additional else ""

        ability_text = f"""{idx}. {ability.get('name')} ({ability.get('type')})
            Description: {ability.get('description')}
            {"Details: " + additional_text if additional_text else ""}"""
        ability_texts.append(ability_text)

    chunk_text = f"""Hero Name: {name}
        Real Name: {real_name}
        Role: {role}
        Attack Type: {attack_type}
        Difficulty: {difficulty}

        Abilities:
        {chr(10).join(ability_texts)}"""

    return {
        "_id": id,
        "chunk_text": chunk_text,
        "category": [
            f"hero_name: {name}",
            f"role: {role}",
            f"attack_type: {attack_type}",
            f"difficulty: {difficulty}"
        ]
    }

def hero_meta_update():
    """
    Creates a new namespace in pinecone and adds every hero with a default entry into the namespace.
    """

    with open('../data/Official_Hero_WR.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        records = []
        for row in reader:
            rec = {
                "_id": f"meta_{row['Name']}",
                "chunk_text": 'This guy is cracked yo',
                "category": [
                    f"hero_name: {row['Name']}"
                ]       
            }
            records.append(rec)

    index.upsert_records('hero_meta', records)


def check_diff():
    t1 = []
    with open('../data/hero_leaderboard.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            t1.append(row['name'])

    t2 = []
    with open('../data/Official_Hero_WR.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            t2.append(row['Name'])

    for name in t2:
        lowercase_name = name.lower()
        if lowercase_name not in t1:
            print(f'Missing {name}')

    for name in t1:
        if name not in t2:
            print(f'Extra {name}')


if __name__ == '__main__':
    # update_heroes_pinecone('daredevil')
    check_diff()