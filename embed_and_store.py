from pathlib import Path
from utils import safe_filename_to_url, extract_keywords
import openai
import datetime
import config
from supabase import create_client, Client

EXTRACT_TEXT_DIR = Path('extract_text')

SUPABASE_URL = config.SUPABASE_URL
SUPABASE_KEY = config.SUPABASE_KEY
OPENAI_API_KEY = config.OPENAI_API_KEY

def get_openai_embedding(text):
    if not OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY not set')
    openai.api_key = OPENAI_API_KEY
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def store_in_supabase_vector(url, text, embedding_fn):
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase credentials not set. Skipping storage.")
        return
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    chunk_size = 5000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for idx, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
        embedding = embedding_fn(chunk)
        tags = extract_keywords(chunk, 10)
        metadata = {
            "url": url,
            "part": idx + 1,
            "date": now,
            "tag": tags
        }
        data = {
            "content": chunk,
            "embedding": embedding,
            "metadata": metadata
        }
        supabase.table("n8n_test").insert(data).execute()

def embed_and_store_all():
    for txt_file in EXTRACT_TEXT_DIR.glob('*.txt'):
        print(f"Embedding and storing {txt_file.name}")
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                text = f.read()
            if not text.strip():
                print(f"No text in {txt_file.name}, skipping.")
                continue
            url = safe_filename_to_url(txt_file.stem)
            store_in_supabase_vector(url, text, get_openai_embedding)
        except Exception as e:
            print(f"Failed to embed/store for {txt_file}: {e}") 