import os 
from dotenv import load_dotenv

from supabase import Client, create_client

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

if not all([SUPABASE_URL, SUPABASE_KEY, SUPABASE_JWT_SECRET, SUPABASE_BUCKET]):
    raise EnvironmentError("Missing Supabase environment variables")

#Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)