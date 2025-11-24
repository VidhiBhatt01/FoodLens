import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
from model.predictor import recommend
from backend.events import add_event, fetch_events
from backend.supabase_client import get_client
from backend.subscribers import add_subscriber

st.set_page_config(page_title="FoodLens", layout="wide")

# Displaying app branding
st.markdown("""
<h1 style='text-align:center; margin-bottom:0;'>🍕🔍 FoodLens</h1>
<p style='text-align:center; font-size:1.2rem; color:#666;'>Saving Food. Feeding Bruins.</p>
<br>
""", unsafe_allow_html=True)

st.title("FoodLens: UCLA Food Sharing & Planning")

# Mapping building names to coordinates
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

# Initializing events in session state
if "events" not in st.session_state:
    st.session_state["events"] = []

# Creating main tabs
tab_add, tab_browse, tab_predict, tab_feedback = st.tabs(["Add Event", "Browse Events", "Food Surplus Predictor", "Contact Us"])

# ----------------- TAB A: ADD EVENT -----------------
with tab_add:
    st.subheader("Add a Free Food Event")

    with st.form("add_event_form"):
        title = st.text_input("Event title (optional)")
        building = st.selectbox("Building", list(BUILDING_COORDS.keys()))
        zone = st.selectbox("Zone", ["north","south","east","west"])
        event_type = st.selectbox("Event type", ["club","seminar","fair","career_fair"])
        diet = st.selectbox("Diet", ["vegan","vegetarian","non-vegetarian","mixed"])
        food_desc = st.text_input("Food description (e.g., pizza, sandwiches)")
        collect_mode = st.selectbox("Collect mode", ["Until supplies last", "Until specific time"])
        collect_until_time = st.time_input("Until what time?", disabled=(collect_mode=="Until supplies last"))
        uploaded_image = st.file_uploader("Upload event image (optional)", type=["png","jpg","jpeg"])
        submitted = st.form_submit_button("Add Event")

    if submitted:
        img_path = None
        if uploaded_image:
            import uuid
            ext = uploaded_image.name.split(".")[-1]
            file_name = f"{uuid.uuid4()}.{ext}"

            # Upload to Supabase Storage
            sb = get_client()
            sb.storage.from_("event-images").upload(
                file_name, uploaded_image.getvalue(), file_options={"content-type": uploaded_image.type}
            )
            img_path = sb.storage.from_("event-images").get_public_url(file_name)

        new_event = {
            "building": building,
            "zone": zone,
            "event_type": event_type,
            "diet": diet,
            "food_desc": food_desc,
            "collect_mode": collect_mode,
            "collect_until_time": collect_until_time.strftime("%H:%M") if collect_mode=="Until specific time" else "",
            "image_url": img_path,
            "is_active": True
        }

        add_event(new_event)
        st.success("Event added (persistent)!")

    # Adding event closure functionality
    st.subheader("Close an Event")
    active_events = [e for e in st.session_state["events"] if e["is_active"]]
    if active_events:
        event_to_close = st.selectbox("Select event to close", [f"#{e['id']} - {e['building']}" for e in active_events])
        reason = st.text_input("Reason for closing (e.g., food over, moved)")
        if st.button("Close selected event"):
            target_id = int(event_to_close.split("#")[1].split(" ")[0])
            for e in st.session_state["events"]:
                if e["id"] == target_id:
                    e["is_active"] = False
                    e["reason_closed"] = reason
            st.success(f"Event {event_to_close} closed.")
    else:
        st.info("No active events to close.")

# ----------------- TAB B: BROWSE EVENTS -----------------
with tab_browse:
    st.subheader("Browse Active Free Food Events")

    # Setting up login simulation for notifications
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
        st.markdown("**Notification preferences (simulated emails):**")
        pref_zone = st.multiselect("Preferred zones", ["north","south","east","west"], default=["north","south","east","west"])
        pref_diet = st.multiselect("Preferred diets", ["vegan","vegetarian","non-vegetarian","mixed"], default=["vegan","vegetarian","non-vegetarian","mixed"])
        email = st.text_input("Email address (for simulated notifications)")

        # Validating email format in real-time
        import re
        email_valid = False
        if email.strip() != "":
            pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
            if re.match(pattern, email.strip()):
                email_valid = True
                st.success("Valid email ✔")
            else:
                st.error("Invalid email format. Example: name@example.com")

        subscribed = st.button("Subscribe to email notifications")
        notif_prefs = {
            "username": username,
            "email": email,
            "zones": pref_zone,
            "diets": pref_diet,
            "subscribed": False
        }

        if subscribed:
            if not email_valid:
                st.error("Please enter a valid email address before subscribing.")
            else:
                add_subscriber(username, email, pref_zone, pref_diet)
                st.success(f"Subscribed! Notifications will be sent to {email}.")
    else:
        st.info("You can still browse all events without logging in.")

    # Adding browse filters
    st.markdown("**Browse filters:**")
    f_zone = st.multiselect("Filter by zone", ["north","south","east","west"], default=["north","south","east","west"])
    f_diet = st.multiselect("Filter by diet", ["vegan","vegetarian","non-vegetarian","mixed"], default=["vegan","vegetarian","non-vegetarian","mixed"])
    events = fetch_events()
    active_events = [e for e in events if e["is_active"]
                     and e["zone"] in f_zone 
                     and e["diet"] in f_diet]

    # Creating interactive map with markers
    focus = st.session_state.get("focus_event")
    if focus:
        lat, lon = BUILDING_COORDS[focus["building"]]
        m = folium.Map(location=[lat, lon], zoom_start=18)
        folium.Marker(
            location=[lat, lon],
            popup=f"#{focus['id']} — {focus['building']}",
            tooltip="Focused Event",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        st.markdown(f"[Open in Google Maps]({gmaps_url})")
    else:
        m = folium.Map(location=[34.0689, -118.4452], zoom_start=16)

    # Adding markers for all active events
    for e in active_events:
        if focus and e["id"] == focus["id"]:
            continue
        lat, lon = BUILDING_COORDS.get(e["building"], (34.0689, -118.4452))
        folium.Marker(
            location=[lat, lon],
            popup=f"#{e['id']} - {e['building']} ({e['event_type']})",
            tooltip=e["food_desc"] or "Click for details"
        ).add_to(m)

    st_data = st_folium(m, width=700, height=450)

    # ---------------- ACTIVE EVENTS SECTION ----------------

    st.markdown("### Active Events")



    # Inject CSS for the event card ------------

    st.markdown("""

    <style>

    .event-card {

        background-color:#1e1e1e;

        padding:18px;

        border-radius:10px;

        border:1px solid #333;

        margin-bottom:12px;

        color:white;

        font-family: Inter, sans-serif;

    }

    .event-title {

        font-size:1.1rem;

        font-weight:600;

        margin-bottom:8px;

    }

    .event-row { margin:4px 0; }

    .event-label { font-weight:600; color:#bbdefb; }

    .tag {

        display:inline-block;

        padding:3px 7px;

        border-radius:5px;

        margin-right:6px;

        margin-bottom:4px;

        font-size:0.75rem;

        color:white;

    }

    .tag-zone { background:#4285F4; }

    .tag-diet { background:#00C853; }

    </style>

    """, unsafe_allow_html=True)



    if not active_events:

        st.write("No events match your filters right now.")

    else:

        for e in active_events:

            with st.expander(f"#{e['id']} — {e['building']}", expanded=False):



                # Inject card CSS

                st.markdown("""

                <style>

                .event-card {

                    background-color: #1e1e1e;

                    padding: 18px;

                    margin-bottom: 16px;

                    border-radius: 10px;

                    border: 1px solid #333;

                    color: #f2f2f2;

                    font-family: sans-serif;

                }

                .badge-row {

                    display: flex;

                    gap: 10px;

                    margin-bottom: 12px;

                }

                .badge {

                    padding: 5px 10px;

                    border-radius: 6px;

                    color: white;

                    font-size: 0.8rem;

                    font-weight: 600;

                }

                .badge-zone { background:#4285F4; }

                .badge-diet { background:#00C853; }

                .event-label { font-weight:600; color:#bbdefb; }

                </style>

                """, unsafe_allow_html=True)



                # Render card

                st.markdown(f"""

                <div class='event-card'>

                    <div class='badge-row'>

                        <div class='badge badge-zone'>{e['zone'].capitalize()}</div>

                        <div class='badge badge-diet'>{e['diet']}</div>

                    </div>



                    <p><span class='event-label'>Food:</span> {e['food_desc']}</p>

                    <p><span class='event-label'>Type:</span> {e['event_type']}</p>

                    <p><span class='event-label'>Collect:</span> {e['collect_mode']} {e['collect_until_time'] or ""}</p>

                </div>

                """, unsafe_allow_html=True)



                # Show image if available

                if e.get("image_url"):

                    st.image(e["image_url"], width=300, caption=f"Event #{e['id']} image")



                # Action button

                if st.button(f"Show on map (Event #{e['id']})", key=f"show_map_{e['id']}"):

                    st.session_state["focus_event"] = e

                    st.success(f"Highlighting event #{e['id']} on map...")

    # Simulating email notifications for subscribed users
    if logged_in and active_events:
        st.markdown("### Simulated Email Notifications")
        if st.button("Simulate sending emails for new events"):
            matching_events = [e for e in active_events if e["zone"] in notif_prefs["zones"] and e["diet"] in notif_prefs["diets"]]
            if matching_events:
                st.write(f"User `{username}` would receive notifications for:")
                for e in matching_events:
                    st.write(f"- Event #{e['id']} at {e['building']} ({e['diet']}, {e['zone']})")
                    if e.get("image_path") and os.path.exists(e["image_path"]):
                        st.image(e["image_path"], width=150)
            else:
                st.write("No events match your notification preferences right now.")

# ----------------- TAB C: FOOD SURPLUS PREDICTOR -----------------
with tab_predict:
    st.subheader("Food Surplus Predictor (Interpretable)")
    col1, col2 = st.columns(2)

    with col1:
        # Collecting event details for prediction
        building = st.selectbox("Building", list(BUILDING_COORDS.keys()), key="pred_building")
        zone = st.selectbox("Zone", ["north","south","east","west"], key="pred_zone")
        event_type = st.selectbox("Event type", ["club","seminar","fair","career_fair"], key="pred_event_type")
        day = st.selectbox("Day of week", ["mon","tue","wed","thu","fri"], key="pred_day")
        time = st.selectbox("Time", ["09:00","12:00","15:00","18:00","20:00"], key="pred_time")
        rsvps = st.number_input("RSVP count", min_value=0, max_value=500, value=150, key="pred_rsvps")
        planned_food = st.number_input("Planned food quantity (e.g., sandwiches)", min_value=0, max_value=600, value=160, key="pred_food")

        if st.button("Get Recommendation"):
            result = recommend(building=building, zone=zone, event_type=event_type, day=day, time=time, rsvps=rsvps, planned_food=planned_food)
            st.session_state["pred_result"] = result

    with col2:
        # Displaying prediction results and explanations
        if "pred_result" in st.session_state:
            res = st.session_state["pred_result"]
            st.markdown("### Recommendation")
            st.write(f"Predicted attendance: **{res['predicted_attendance']}**")
            st.write(f"Planned food: **{planned_food}**")
            st.write(f"Recommended food: **{res['recommended_food']}**")
            if res["reduction"] > 0:
                st.write(f"Suggested reduction: **{res['reduction']}** portions to reduce surplus risk.")
            else:
                st.write("No reduction recommended. Plan already looks conservative.")
            st.markdown("### Explanation")
            for line in res["explanation"]:
                st.write(f"- {line}")
        else:
            st.info("Fill the form and click 'Get Recommendation' to see model output.")

        # Displaying user testimonials
        st.markdown("### User Testimonials")
        st.markdown("""
        <style>
        .testimonial-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
            color: #155724;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""<div class='testimonial-box'>
                    <div style='color:#2e7d32; font-size:1.1rem;'>⭐⭐⭐⭐⭐</div>
                    "The prediction helped us cut costs and avoid waste!" — UCLA ACM Officer 💙
                    </div>""", unsafe_allow_html=True)
        st.markdown("""<div class='testimonial-box'>
                    <div style='color:#2e7d32; font-size:1.1rem;'>⭐⭐⭐⭐⭐</div>
                    "Super useful. The explanation makes it trustworthy." — Grad Student CS 👩‍💻
                    </div>""", unsafe_allow_html=True)
        st.markdown("""<div class='testimonial-box'>
                    <div style='color:#2e7d32; font-size:1.1rem;'>⭐⭐⭐⭐⭐</div>
                    "We stopped over-ordering by 20%. Love the transparency!" — Club Treasurer 🎓
                    </div>""", unsafe_allow_html=True)

# ----------------- TAB D: FEEDBACK FORM -----------------
with tab_feedback:
    st.subheader("Contact / Feedback")
    name = st.text_input("Your name")
    email = st.text_input("Your email")
    msg = st.text_area("Message")

    if st.button("Submit feedback"):
        sb = get_client()
        sb.table("feedback").insert({
            "name": name,
            "email": email,
            "message": msg
        }).execute()

        st.success("Thank you! Your feedback has been recorded.")

# Displaying footer
st.markdown("""
<br><br>
<div style='text-align:center; color:gray; padding:20px; font-size:0.9rem;'>
    Made with ❤️ by Vidhi (MS CS @ UCLA – Fall 2025)
</div>
""", unsafe_allow_html=True)
