import os
from supabase import create_client
from openai import OpenAI

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
client = OpenAI()

def get_embedding(text: str):
    return client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding

def search_knowledge(query: str, k=5):
    embedding = get_embedding(query)
    response = supabase.rpc("match_documents", {"query_embedding": embedding,"match_count": k}).execute()
    return response.data if response.data else []
