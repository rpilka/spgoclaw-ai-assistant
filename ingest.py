import os
from supabase import create_client
from openai import OpenAI

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
client = OpenAI()

def get_embedding(text):
    return client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding

def add_chunk(text):
    emb = get_embedding(text)
    supabase.table("kb_chunks").insert({"content": text,"source": "FAQ","url": "https://spgoclaw.pl"}).execute()

faq = ["Godziny sekretariatu 08:00–15:00","Dokumenty w zakładce Dokumenty","Rekrutacja w zakładce Rekrutacja"]
for item in faq:
    add_chunk(item)

print("FAQ added")
