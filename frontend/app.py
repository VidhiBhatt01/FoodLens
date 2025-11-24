import sys
import os

# Allow importing backend/ and model/ from frontend/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import folium
from streamlit_folium import st_folium

from model.predictor import recommend
from backend.events import add_event, fetch_events, deactivate_event
from backend.supabase_client import get_client
from backend.subscribers import add_subscriber

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="FoodLens", layout="wide")

# ----------------- BRANDING HEADER -----------------
st.markdown(
    """
<h1 style='text-align:center; margin-bottom:0;'>🍕🔍 FoodLens</h1>
<p style='text-align:center; font-size:1.2rem; color:#666;'>Saving Food. Feeding Bruins.</p>
<br>
""",
    unsafe_allow_html=True,
)

st.title("FoodLens: UCLA Food Sharing & Planning")

# ----------------- BUILDING COORDS -----------------
BUILDING_COORDS = {
    "Boelter Hall": (34.0689, -118.4441),
    "Math Sciences": (34.0686, -118.4429),
    "Engineering VI": (34.0683, -118.4455),
    "Royce Hall": (34.0722, -118.4421),
    "Haines Hall": (34.0713, -118.4410),
    "Kaplan Hall": (34.0718, -118.4419),
    "Anderson": (34.0736, -118.4422),
    "UCLA Law": (34.0731, -118.4410),
    "Gonda": (34.0698, -118.4490),
    "Pauley Pavilion": (34.0703, -118.4469),
    "Hedrick Hall": (34.0716, -118.4503),
    "Sproul Hall": (34.0710, -118.4509),
}

# ----------------- TABS -----------------
tab_add, tab_browse, tab_predict, tab_feedback = st.tabs(
    ["Add Event", "Browse Events", "Food Surplus Predictor", "Contact Us"]
)

# ======================================================
# TAB A: ADD EVENT
# ======================================================
with tab_add:
    st.subheader("Add a Free Food Event")

    with st.form("add_event_form"):
        title = st.text_input("Event title (optional)")
        building = st.selectbox("Building", list(BUILDING_COORDS.keys()))
        zone = st.selectbox("Zone", ["north", "south", "east", "west"])
        event_type = st.selectbox("Event type", ["club", "seminar", "fair", "career_fair"])
        diet = st.selectbox("Diet", ["vegan", "vegetarian", "non-vegetarian", "mixed"])
        food_desc = st.text_input("Food description (e.g., pizza, sandwiches)")
        collect_mode = st.selectbox("Collect mode", ["Until supplies last", "Until specific time"])
        collect_until_time = st.time_input(
            "Until what time?", disabled=(collect_mode == "Until supplies last")
        )
        uploaded_image = st.file_uploader("Upload event image (optional)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("Add Event")

    if submitted:
        img_path = None
        if uploaded_image:
            import uuid

            ext = uploaded_image.name.split(".")[-1]
            file_name = f"{uuid.uuid4()}.{ext}"

            sb = get_client()

            sb.storage.from_("event-images").upload(
                file_name,
                uploaded_image.getvalue(),
                file_options={"content-type": uploaded_image.type},
            )

            # More reliable public URL
            base = sb.storage.from_("event-images").get_public_url(file_name)
            img_path = (
                base if base.startswith("http")
                else f"{sb.supabase_url}/storage/v1/object/public/event-images/{file_name}"
            )

        new_event = {
            "building": building,
            "zone": zone,
            "event_type": event_type,
            "diet": diet,
            "food_desc": food_desc,
            "collect_mode": collect_mode,
            "collect_until_time": (
                collect_until_time.strftime("%H:%M")
                if collect_mode == "Until specific time"
                else ""
            ),
            "image_url": img_path,
            "is_active": True,
        }

        add_event(new_event)
        st.success("Event added (persistent via Supabase)!")

    # -------- CLOSE EVENT --------
    st.subheader("Close an Event")

    all_events = fetch_events()
    active_events_close = [e for e in all_events if e.get("is_active")]

    if active_events_close:
        # Sequential numbering
        numbered = [(i + 1, e) for i, e in enumerate(active_events_close)]
        label_options = [f"{num}. {e['building']}" for num, e in numbered]
        selected_label = st.selectbox("Select event to close", label_options)
        close_reason = st.text_input("Reason for closing (e.g., food over, moved)")

        if st.button("Close selected event"):
            idx = int(selected_label.split(".")[0]) - 1
            event_id = active_events_close[idx]["id"]
            deactivate_event(event_id, close_reason)
            st.success(f"Closed event: {selected_label}")

    else:
        st.info("No active events to close.")

# ======================================================
# TAB B: BROWSE EVENTS
# ======================================================
with tab_browse:
    st.subheader("Browse Active Free Food Events")

    # Login simulation
    st.markdown("**Login for email notification preferences (simulated):**")
    col1, col2, col3 = st.columns(3)
    with col1:
        username = st.text_input("Username")
    with col2:
        password = st.text_input("Password", type="password")
    with col3:
        logged_in = st.checkbox("Simulate login")

    notif_prefs = {}

    if logged_in:
        st.success(f"Logged in as {username} (simulated).")
        pref_zone = st.multiselect(
            "Preferred zones", ["north", "south", "east", "west"],
            default=["north", "south", "east", "west"]
        )
        pref_diet = st.multiselect(
            "Preferred diets",
            ["vegan", "vegetarian", "non-vegetarian", "mixed"],
            default=["vegan", "vegetarian", "non-vegetarian", "mixed"],
        )
        email = st.text_input("Email address (for simulated notifications)")

        import re
        email_valid = re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email or "")

        if email and email_valid:
            st.success("Valid email ✔")
        elif email:
            st.error("Invalid email format. Example: name@example.com")

        if st.button("Subscribe to email notifications"):
            if not email_valid:
                st.error("Please enter a valid email.")
            else:
                add_subscriber(username, email, pref_zone, pref_diet)
                st.success(f"Subscribed! Notifications will go to {email}.")

        notif_prefs = {"zones": pref_zone, "diets": pref_diet}

    else:
        st.info("You can browse events without logging in.")

    # Filters
    st.markdown("**Browse filters:**")
    f_zone = st.multiselect(
        "Filter by zone", ["north", "south", "east", "west"],
        default=["north", "south", "east", "west"]
    )
    f_diet = st.multiselect(
        "Filter by diet",
        ["vegan", "vegetarian", "non-vegetarian", "mixed"],
        default=["vegan", "vegetarian", "non-vegetarian", "mixed"],
    )

    events = fetch_events()
    active_events = [
        e for e in events
        if e.get("is_active") and e.get("zone") in f_zone and e.get("diet") in f_diet
    ]

    # Sequential numbering for display
    for i, e in enumerate(active_events):
        e["display_id"] = i + 1

    # Map
    focus = st.session_state.get("focus_event")
    if focus:
        lat, lon = BUILDING_COORDS.get(focus["building"], (34.0689, -118.4452))
        m = folium.Map(location=[lat, lon], zoom_start=18)
        folium.Marker(
            location=[lat, lon],
            popup=f"{focus['display_id']} — {focus['building']}",
            tooltip="Focused Event",
            icon=folium.Icon(color="red"),
        ).add_to(m)
    else:
        m = folium.Map(location=[34.0689, -118.4452], zoom_start=16)

    for e in active_events:
        if focus and e["id"] == focus["id"]:
            continue
        lat, lon = BUILDING_COORDS.get(e["building"], (34.0689, -118.4452))
        folium.Marker(
            location=[lat, lon],
            popup=f"{e['display_id']} - {e['building']} ({e['event_type']})",
            tooltip=e["food_desc"],
        ).add_to(m)

    st_folium(m, width=700, height=450)

    # Cards UI
    st.markdown("### Active Events")
    st.markdown(
        """
<style>
.event-card {
    background-color: #1e1e1e;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #333;
    margin-bottom: 12px;
    color: #f2f2f2;
}
.badge-row { display: flex; gap: 8px; margin: 6px 0 12px 0; }
.badge { padding: 5px 12px; border-radius: 20px; color:white; font-size:0.75rem; }
.badge-zone { background:#4285F4; }
.badge-diet { background:#00C853; }
.event-label { font-weight:600; color:#bbdefb; }
</style>
""",
        unsafe_allow_html=True,
    )

    if not active_events:
        st.write("No events match your filters right now.")
    else:
        for e in active_events:
            with st.expander(f"{e['display_id']} — {e['building']}", expanded=False):
                st.markdown(
                    f"""
<div class="event-card">
    <div class="event-title">{e['display_id']} – {e['building']}</div>
    <div class="badge-row">
        <div class="badge badge-zone">{e['zone'].capitalize()}</div>
        <div class="badge badge-diet">{e['diet']}</div>
    </div>
    <div class="event-row"><span class="event-label">Food:</span> {e['food_desc']}</div>
    <div class="event-row"><span class="event-label">Type:</span> {e['event_type']}</div>
    <div class="event-row"><span class="event-label">Collect:</span> {e['collect_mode']} {e['collect_until_time']}</div>
</div>
""",
                    unsafe_allow_html=True,
                )

                if e.get("image_url"):
                    st.image(e["image_url"], width=260, caption=f"Event {e['display_id']} image")

                if st.button(f"Show on map (Event {e['display_id']})", key=f"map_btn_{e['id']}"):
                    st.session_state["focus_event"] = e
                    st.success(f"Highlighted event {e['display_id']} on map.")

# ======================================================
# TAB C: FOOD SURPLUS PREDICTOR
# ======================================================
with tab_predict:
    st.subheader("Food Surplus Predictor (Interpretable)")

    col1, col2 = st.columns(2)

    with col1:
        building = st.selectbox("Building", list(BUILDING_COORDS.keys()), key="pred_building")
        zone = st.selectbox("Zone", ["north", "south", "east", "west"], key="pred_zone")
        event_type = st.selectbox("Event type", ["club", "seminar", "fair", "career_fair"], key="pred_event_type")
        day = st.selectbox("Day of week", ["mon", "tue", "wed", "thu", "fri"], key="pred_day")
        time = st.selectbox("Time", ["09:00", "12:00", "15:00", "18:00", "20:00"], key="pred_time")
        rsvps = st.number_input("RSVP count", min_value=0, max_value=500, value=150, key="pred_rsvps")
        planned_food = st.number_input(
            "Planned food quantity (e.g., sandwiches)",
            min_value=0, max_value=600, value=160, key="pred_food",
        )

        if st.button("Get Recommendation"):
            st.session_state["pred_result"] = recommend(
                building=building, zone=zone, event_type=event_type,
                day=day, time=time, rsvps=rsvps, planned_food=planned_food
            )

    with col2:
        if "pred_result" in st.session_state:
            res = st.session_state["pred_result"]
            st.markdown("### Recommendation")
            st.write(f"Predicted attendance: **{res['predicted_attendance']}**")
            st.write(f"Planned food: **{planned_food}**")
            st.write(f"Recommended food: **{res['recommended_food']}**")

            if res["reduction"] > 0:
                st.write(f"Suggested reduction: **{res['reduction']}** portions.")
            else:
                st.write("No reduction recommended — already conservative.")

            st.markdown("### Explanation")
            for line in res["explanation"]:
                st.write(f"- {line}")
        else:
            st.info("Fill the form and click 'Get Recommendation'.")

# ======================================================
# TAB D: FEEDBACK FORM
# ======================================================
with tab_feedback:
    st.subheader("Contact / Feedback")

    name = st.text_input("Your name")
    email = st.text_input("Your email")
    msg = st.text_area("Message")

    if st.button("Submit feedback"):
        sb = get_client()
        sb.table("feedback").insert(
            {"name": name, "email": email, "message": msg}
        ).execute()
        st.success("Thank you! Your feedback has been recorded.")

# ----------------- FOOTER -----------------
st.markdown(
    """
<br><br>
<div style='text-align:center; color:gray; padding:20px; font-size:0.9rem;'>
    Made with ❤️ by Vidhi (MS CS @ UCLA – Fall 2025)
</div>
""",
    unsafe_allow_html=True,
)
