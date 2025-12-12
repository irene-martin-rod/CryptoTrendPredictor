# Pipeline to obtain configuration from .env

from supabase import create_client
import os
from dotenv import load_dotenv

# Load environmental variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
