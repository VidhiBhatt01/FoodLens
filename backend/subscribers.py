from backend.supabase_client import get_client

sb = get_client()

def add_subscriber(username, email, zones, diets):
    sb.table("subscribers").insert({
        "username": username,
        "email": email,
        "zones": zones,
        "diets": diets
    }).execute()
