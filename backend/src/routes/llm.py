from flask import Blueprint, jsonify, request
import requests
from dotenv import load_dotenv
import os
from db.connection import r, openai_client
import csv
from db.connection import index
import json
import uuid
from services.rivals_context import rivals_context, map_context

load_dotenv()

# Access variables
api_key = os.getenv("OPENAI_API_KEY")

llm_bp = Blueprint("llm", __name__)

@llm_bp.route("/", methods=["POST"])
def get_tips():
    """
    Generates personalized tips for a player based on their rank and top heroes/maps.
    
    This endpoint retrieves hero statistics, searches for relevant context from Pinecone,
    fetches win rates and pick rates from CSV data, and uses OpenAI to generate personalized
    gaming tips and identify weak spots.
    
    Request JSON body:
        name (str): The player's username.
        rank (str): The player's current competitive rank.
        topHeroes (list): List of top 3 heroes played by the player.
        topMaps (list): List of top maps played by the player.
    
    Returns:
        dict: JSON response containing:
            tips (list): List of personalized tips and recommendations.
            session_id (str): Unique session ID for conversation continuation.
        Status code 200 on success, 500 on error.
    
    Raises:
        Exception: Catches and returns JSON error response with exception details.
    """
    try:        
        data = request.get_json()
        name = data.get("name")
        rank = data.get("rank")
        stats = data.get("topHeroes")[:3]
        maps = data.get("topMaps")


        search_text = ''
        for hero in stats:
            search_text += str(hero) + '\n'

        results = index.search(
            namespace="__default__", 
            query={
                "inputs": {"text": search_text}, 
                "top_k": 3
            },
            fields=["category", "chunk_text"]
        )

        
        context = ''
        for record in results['result']['hits']:
            if record['_score'] > .3:
                context += str(record['fields']['chunk_text']) + '\n' + str(record['fields']['category'])

        users = ''
        if rank == 'One Above All' or rank == 'Eternity':
            rank = 'Celestial'
        with open('../data/Official_Hero_WR.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    wr_string = rank.split(' ')[0] + ' WR'
                    pr_string = rank.split(' ')[0] + ' PR'
                    if pr_string in row:
                        users += row['Name'] + ': PR - ' + row[pr_string] + ', '
                    else:
                        users += row['Name'] + ': PR - N/A, '
                    if wr_string in row:
                        users += row['Name'] + ': WR - ' + row[wr_string] + '\n'
                    else:
                        users += row['Name'] + ': WR - N/A\n'

        maps_full = []
        
        if maps:
            maps_full = [
            {**m , "name": f"{map_context[m['map_id']]['name']} - {map_context[m['map_id']]['location']} ", "game mode": {map_context[m['map_id']]['game_mode']} }
              for m in maps
              if m['map_id'] in map_context
            ]

        pinecone_prompt = rivals_context['Gen_Prompt'] + f"""     
            \nThe following is information on hero pick rate and win rate across all competitive matches for the rank - {rank}:{users}
            \nHERO CONTEXT:{context}
            
            QUESTION:
            These are my top heroes and my top maps.
            Based on my rank({rank}), give me some tips on how to rank up in competitive and tell me where my weak spots are: {stats}.
            {maps_full}
        """
       
        print(pinecone_prompt)
        response = openai_client.responses.create(
            model="gpt-5.1",
            input= [
            {
                "role": "system",
                "content": """You are an expert on the game Marvel Rivals, who provides advice and information on the game.
                    Only use the context given in the prompt to answer a question.
                    If you do not know the answer, DO NOT GUESS, just say 'Im not sure'
                    IF ANY OF THE CONTENT IS NOT RELEVANT TO MARVEL RIVALS, START WITH 'I cannot reply, Irrelevant content found'.
                    then give your reasoning of what irrelevant content was found/asked.
                    Tips can be however long or short, but please provide at least 5 tips.
                    When answering, never explicitly mention the context you used in your answer, 
                    the reasonings section of the JSON output is reserved for that.
                    Use the reasonings section to list what contexts were used for each tip, no more than two sentences per reasoning.
                    ALWAYS respond only in valid JSON (no extra text).
                    JSON structure MUST match exactly this format:
                    {{
                        "tips": [
                        {{
                            "tip": "tip 1"
                        }},
                        {{
                            "tip": "tip 2"
                        }}
                        ],
                        "reasonings": [
                        {{
                            "reasoning": "reasoning for tip 1"
                        }},
                        {{
                            "reasoning": "reasoning for tip 2"
                        }}
                        ]
                    }} 
                    """,
            },
            {
                "role": "user",
                "content": pinecone_prompt,
            },
            ],
            
        )

        session_id = str(uuid.uuid4())
        #r.set(session_id, response.id)
        
        r.setex(session_id, 3600, response.id) # for expiration timers (1 hour)

        parsed_json = json.loads(response.output_text)  # convert JSON string to Python dict
        tip_list = [tip["tip"] for tip in parsed_json.get("tips", [])]  # extract list of tips
        reasoning_list = [tip["reasoning"] for tip in parsed_json.get("reasonings", [])]  # extract list of reasons
        for reasoning in reasoning_list:
            print("Reasoning: ", reasoning)
        return jsonify({"tips": tip_list, "session_id":session_id}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
    

@llm_bp.route("/conversation", methods=["POST"])
def get_llm_res():
    """
    Continues a conversation with the LLM based on a previous session.
    
    This endpoint handles follow-up questions in an ongoing conversation about Marvel Rivals.
    It determines relevant categories for the question, retrieves appropriate context from
    Pinecone and game knowledge, and generates a response using OpenAI.
    
    Request JSON body:
        text (str): The user's follow-up question.
        session_id (str): The session ID from a previous /get_tips call.
    
    Returns:
        dict: JSON response containing:
            text (str): The LLM's response to the user's question.
        Status code 200 on success, 500 on error.
    
    Raises:
        ValueError: If text is not a string.
        KeyError: If session_id is not found or has expired.
        Exception: Catches and returns JSON error response with exception details.
    """
    try:
        data = request.get_json()

        question = data.get("text")

        if type(question) != str:
            return jsonify({"error": "Please only insert text"}), 500
        
        session = data.get("session_id")
        conv_id = r.get(session)
        if not conv_id:
            return jsonify({"error": "Could not find your llm conversation, it may have expired"}), 500
        
        cats_res = get_categories(question, conv_id)
        cats = [c.strip() for c in cats_res.split(',')]
        context = ''
        print("Prepped: ", cats)

        if 'Hero current meta info' in cats:
            results = index.search(
                namespace="hero_meta", 
                query={
                    "inputs": {"text": question}, 
                    "top_k": 5
                },
                fields=["category", "chunk_text"]
            )
            print('meta results:', results)

            for record in results['result']['hits']:
                if record['_score'] > .25:
                    context += str(record['fields']['chunk_text']) + '\n'

        if 'All heroes' in cats:
            results = index.search(
                namespace="__default__", 
                query={
                    "inputs": {"text": question}, 
                    "top_k": 44
                },
                fields=["category", "chunk_text"]
            )

            for record in results['result']['hits']:
                context += str(record['fields']['category'])+ '\n'

        if "Practice regiments" in cats:
            context += rivals_context['Practice regiments'] + '\n'
            
        if "Team compositions" in cats:
            context += rivals_context['Team compositions'] + '\n'

        if "Terms" in cats:
            context += rivals_context['Terms'] + '\n'

        prompt = f""" Use the following context to answer the user's question.
        CONTEXT: {context}

        QUESTION:{question}"""

        print(prompt)

        second_response = openai_client.responses.create(
            model="gpt-5.1",
            previous_response_id=conv_id,
            input= [
            {
                "role": "system",
                "content": "You are an expert on the game Marvel Rivals, who provides advice and information on the game.\
                    Only use the context given in the prompt to answer a questions. \
                    If there is more context than you need or context not directly relevant to the question, ignore it without making a note of it.\
                    If you do not know the answer, DO NOT GUESS, just say 'Im not sure' \
                    IF ANY OF THE QUESTION CONTENT IS NOT RELEVANT TO MARVEL RIVALS, REPLY WITH 'I cannot reply, Irrelevant content found'.\
                    Reply in plain text format as a single paragraph answer, the paragraph can be very long or very short but it must be one paragraph.",
            },
            {
                "role": "user",
                "content": prompt,
            },
            ],
            
        )

        r.set(session, second_response.id, keepttl=True)

        return jsonify({"text": second_response.output_text}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


def get_categories(question: str, conv_id: str) -> str:
    """
    Determines which knowledge categories are relevant to answer a user's question.
    
    Uses OpenAI to intelligently classify a question and identify which knowledge
    categories (heroes, meta info, game modes, etc.) are needed to provide an accurate
    response about Marvel Rivals.
    
    Args:
        question (str): The user's question about Marvel Rivals.
        conv_id (str): The conversation ID from Redis for maintaining context.
    
    Returns:
        str: A comma-separated string of relevant categories, or special values:
            - "Irrelevant": If the question is not related to Marvel Rivals.
            - "None": If the question can be answered with existing knowledge.
            - Otherwise: Comma-separated list of categories such as:
              "All heroes", "Hero current meta info", "Hero ability info",
              "Game mode rules", "Practice regiments", "Team compositions", "Terms"
    """
            
    categories = ['All heroes', 'Hero current meta info', 'Hero ability info', 'Game mode rules', 'Practice regiments', 'Team compositions', 'Terms']

    cat_prompt = rivals_context['Gen_Prompt'] + f"\n\nQUESTION: {question}"

    categories_response = openai_client.responses.create(
        model="gpt-5.1",
        input= [
            {
                "role": "system",
                "content": f"""Based on the user's question, return a list of the following categories that you believe you will need 
                    information on to be able to answer correctly. 
                    If the question is not relevant to Marvel Rivals then reply with the single word - Irrelevant. 
                    If you know you can answer with only the context you already have, reply with the single word - None.
                    All other answers should be plain text with commas separating each category, NO ADDITIONAL TEXT.
                    Include the "All heroes" category when you will need basic information on all heroes in the game, for example if you
                    are asked to create a team composition.
                    Include the "Terms" category when there is a term used by the user that you're not 100% confident on the definition of but 
                    still likely relates to gaming/ Marvel Rivals.
                    
                    Example interactions:
                    1a. User: "What color are Groot's walls?"
                    1b. Output: "Irrelevant"
                    2a. User: "Make me a team composition that works well for Domination."
                    2b. Output: "Game mode rules, Team compositions, All heroes"
                    3a. User: "What healers are best to pattycake with?"
                    3b. Output: "Hero current meta info, Terms"
                    
                    Categories: {categories}""",
            },
            {
                "role": "user",
                "content": cat_prompt,
            },
        ],       
    )

    print("Categories output: ", categories_response.output_text)
    return categories_response.output_text