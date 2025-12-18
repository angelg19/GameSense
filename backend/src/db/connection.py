from dotenv import load_dotenv
import os
import pymongo
import sys
from pinecone import Pinecone
import redis
from openai import OpenAI

# Gather the necessary keys
load_dotenv()
mongo_uri = os.getenv("DB_CONNECTION_STRING")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

# Create a new instance of our mongo client to access the database
try:
  client = pymongo.MongoClient(mongo_uri)
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)

# Use the database named "gamesense"
db = client["gamesense"]

# Create a new instance of an OpenAI client which we will use to query our LLM.
openai_client = OpenAI()

# Create a new instance of our pinecone index to be used to store and retrieve Marvel Rivals content. 
pc = Pinecone(api_key=pinecone_api_key)
index_name = "rivals-knowledge-base"
if not pc.has_index(index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"llama-text-embed-v2",
            "field_map":{"text": "chunk_text"}
        }
    )
index = pc.Index(index_name)

# Create a new instance of redis to be used to manage LLM conversation threads
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
