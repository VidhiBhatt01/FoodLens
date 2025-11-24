import sys
import os

# Allow importing backend/ and model/
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
st.markdown("""
<h1 style='text-align:center; margin-bottom:0;'>🍕🔍 FoodLens</h1>
<p style='text-align:center; font-size:1.2rem; color:#666;'>Saving Food. Feeding Bruins.</p>
<br>
""", unsafe_allow_html=True)

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
        building = st.selectbox("Building", list(BUILDING_COORDS.keys()))
        zone = st.selectbox("Zone", ["north", "south", "east", "west"])
        event_type = st.selectbox("Event type", ["club", "seminar", "fair", "career_fair"])
        diet = st.selectbox("Diet", ["vegan", "vegetarian", "non-vegetarian", "mixed"])
        food_desc = st.text_input("Food description (e.g., pizza, sandwiches)")
        collect_mode = st.selectbox("Collect mode", ["Until supplies last", "Until specific time"])
        collect_until_time = st.time_input(
            "Until what time?", disabled=(collect_mode == "Until supplies last")
        )
        uploaded_image = st.file_uploader("Upload event image", type=["png", "jpg", "jpeg"])
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
            # Build stable public URL
            base = sb.storage.from_("event-images").get_public_url(file_name)
            img_path = base if base.startswith("http") else \
                f"{sb.supabase_url}/storage/v1/object/public/event-images/{file_name}"

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
        st.success("Event added!")

    # --- CLOSE EVENT ---
    st.subheader("Close an Event")
    all_events = fetch_events()
    active_events_close = [e for e in all_events if e.get("is_active")]

    if active_events_close:
        numbered = [(i + 1, e) for i, e in enumerate(active_events_close)]
        label_options = [f"{num}. {e['building']}" for num, e in numbered]
        selected_label = st.selectbox("Select event to close", label_options)
        close_reason = st.text_input("Reason")

        if st.button("Close selected event"):
            idx = int(selected_label.split(".")[0]) - 1
            event_id = active_events_close[idx]["id"]
            deactivate_event(event_id, close_reason)
            st.success(f"Closed event {selected_label}")
    else:
        st.info("No active events.")

# ======================================================
# TAB B: BROWSE EVENTS
# ======================================================
with tab_browse:
    st.subheader("Browse Active Free Food Events")

    # Filters
    f_zone = st.multiselect("Filter by zone", ["north", "south", "east", "west"],
                            default=["north", "south", "east", "west"])
    f_diet = st.multiselect("Filter by diet", ["vegan", "vegetarian", "non-vegetarian", "mixed"],
                            default=["vegan", "vegetarian", "non-vegetarian", "mixed"])

    events = fetch_events()
    active_events = [
        e for e in events
        if e.get("is_active") and e.get("zone") in f_zone and e.get("diet") in f_diet
    ]

    # Sequential display numbering
    for i, e in enumerate(active_events):
        e["display_id"] = i + 1

    # --- Map ---
    focus = st.session_state.get("focus_event")

    if focus:
        lat, lon = BUILDING_COORDS.get(focus["building"], (34.0689, -118.4452))
        m = folium.Map(location=[lat, lon], zoom_start=18)
        folium.Marker(
            location=[lat, lon],
            popup=f"{focus['display_id']} — {focus['building']}",
            tooltip="Focused Event",
            icon=folium.Icon(color="red")
        ).add_to(m)
    else:
        m = folium.Map(location=[34.0689, -118.4452], zoom_start=16)

    for e in active_events:
        if focus and e["id"] == focus["id"]:
            continue
        lat, lon = BUILDING_COORDS[e["building"]]
        folium.Marker(
            location=[lat, lon],
            popup=f"{e['display_id']} - {e['building']} ({e['event_type']})",
            tooltip=e["food_desc"],
        ).add_to(m)

    st_folium(m, width=700, height=450)

    # --- Cards ---
    st.markdown("### Active Events")
    if not active_events:
        st.write("No events match your filters right now.")
    else:
        for e in active_events:
            with st.expander(f"{e['display_id']} — {e['building']}", expanded=False):
                st.write(f"**Food:** {e['food_desc']}")
                st.write(f"**Type:** {e['event_type']}")
                st.write(f"**Collect:** {e['collect_mode']} {e['collect_until_time']}")

                if e.get("image_url"):
                    st.image(e["image_url"], width=260)

                # --- SHOW ON MAP + GOOGLE MAPS LINK ---
                if st.button(f"Show on map (Event {e['display_id']})", key=f"map_btn_{e['id']}"):
                    st.session_state["focus_event"] = e
                    lat, lon = BUILDING_COORDS[e["building"]]
                    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                    st.markdown(f"[Open in Google Maps]({gmaps_url})")
                    st.success(f"Highlighted event {e['display_id']} on map.")

# ======================================================
# TAB C: FOOD SURPLUS PREDICTOR
# ======================================================
with tab_predict:
    st.subheader("Food Surplus Predictor (Interpretable)")

    col1, col2 = st.columns(2)

    with col1:
        building = st.selectbox("Building", list(BUILDING_COORDS.keys()))
        zone = st.selectbox("Zone", ["north", "south", "east", "west"])
        event_type = st.selectbox("Event type", ["club", "seminar", "fair", "career_fair"])
        day = st.selectbox("Day", ["mon", "tue", "wed", "thu", "fri"])
        time = st.selectbox("Time", ["09:00", "12:00", "15:00", "18:00", "20:00"])
        rsvps = st.number_input("RSVP count", 0, 500, 150)
        planned_food = st.number_input("Planned food", 0, 600, 160)

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
            st.write(f"Recommended food: **{res['recommended_food']}**")

            if res["reduction"] > 0:
                st.write(f"Reduce by **{res['reduction']} portions**")
            else:
                st.write("No reduction needed.")

            st.markdown("### Explanation")
            for line in res["explanation"]:
                st.write(f"- {line}")
        else:
            st.info("Fill the form to see predictions.")

    # --- ALWAYS SHOW TESTIMONIALS ---
    st.markdown("### User Testimonials")
    st.markdown("""
    <div style='background:#d4edda; padding:15px; border-radius:6px; margin-bottom:10px;'>
      ⭐⭐⭐⭐⭐ – "The prediction helped us cut costs and avoid waste!" — UCLA ACM Officer
    </div>
    <div style='background:#d4edda; padding:15px; border-radius:6px; margin-bottom:10px;'>
      ⭐⭐⭐⭐⭐ – "Super useful. The explanation makes it trustworthy." — Grad Student CS
    </div>
    <div style='background:#d4edda; padding:15px; border-radius:6px; margin-bottom:10px;'>
      ⭐⭐⭐⭐⭐ – "We stopped over-ordering by 20%." — Club Treasurer
    </div>
    """, unsafe_allow_html=True)

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
        sb.table("feedback").insert({"name": name, "email": email, "message": msg}).execute()
        st.success("Thank you! Your feedback has been recorded.")

# ----------------- FOOTER -----------------
st.markdown("""
<br><br>
<div style='text-align:center; color:gray; padding:20px; font-size:0.9rem;'>
    Made with ❤️ by Vidhi (MS CS @ UCLA – Fall 2025)
</div>
""", unsafe_allow_html=True)
