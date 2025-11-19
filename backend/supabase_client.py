import os

from dotenv import load_dotenv
from supabase import create_client, Client

try:
    import streamlit as st
except ImportError:
    st = None

load_dotenv()


def _get_supabase_credentials():
    # Try Streamlit secrets first (cloud)
    if st is not None and hasattr(st, "secrets"):
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if url and key:
            return url, key

    # Fallback to env variables (.env or system env)
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    return url, key


SUPABASE_URL, SUPABASE_KEY = _get_supabase_credentials()

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase environment variables. Check .env or Streamlit secrets.")


def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)