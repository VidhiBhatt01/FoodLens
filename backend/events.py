from backend.supabase_client import get_client

sb = get_client()

def fetch_events():
    res = sb.table("events").select("*").order("created_at", desc=True).execute()
    return res.data or []


def add_event(event_dict):
    sb.table("events").insert(event_dict).execute()


def deactivate_event(event_id, reason=None):
    sb.table("events").update({"is_active": False, "close_reason": reason}).eq("id", event_id).execute()