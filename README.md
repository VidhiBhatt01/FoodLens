<h1 align="center">FoodLens 🍕🔍</h1>
<!-- Banner -->
<p align="center">
  <img src="https://img.shields.io/badge/FoodLens-UCLA%20Free%20Food%20Finder-005587?style=for-the-badge&logo=leaflet&logoColor=white" alt="FoodLens Banner">
</p>

<p align="center">
  <i>Reducing food waste. Empowering students. Built with ethical and interpretable AI.</i>
</p>

<!-- Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
  <img src="https://img.shields.io/badge/Streamlit-Deployable-FF4B4B.svg">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB.svg">
  <img src="https://img.shields.io/badge/Model-Interpretable%20ML-blue.svg">
  <img src="https://img.shields.io/badge/Status-Active-success">
</p>

FoodLens is a campus-wide platform to reduce food waste by connecting surplus event food with students in real time. Designed with transparency, safety, and ethical AI principles inspired by UCLA CS 269.

---

## Overview 🌿

FoodLens enables event organizers to quickly post surplus food availability on campus, helping students find free food while reducing waste. Students can browse active events, customize notification preferences, and view event locations on an interactive UCLA map.

An interpretable machine-learning predictor estimates expected attendance to help organizers avoid over-ordering, maintaining transparency and fairness throughout the system. All content persists in Supabase (events, subscribers, feedback, and media assets) so the experience feels real, not just a Streamlit demo.

---

## Documentation 📄
Full project documentation is available in the `docs/` directory:

- **ARCHITECTURE.md** – System design and component interactions  
- **PROJECT_STRUCTURE.md** – Repository layout and file-level overview  
- **SETUP.md** – Environment setup, Supabase configuration, and run instructions  
- **ACADEMIC_ALIGNMENT.md** – CS 269 alignment, interpretability grounding, and ethics framing  

These documents provide a deeper look into the system beyond what is covered in this README.

---

## Features ✨

• Add/close events with Supabase persistence + storage-backed image uploads  
• Browse active events through collapsible cards synced to a Leaflet map  
• Google Maps deep links + focus buttons to instantly re-center the map  
• Optional login simulation with validated email + preference-based subscriptions  
• Transparent attendance predictor powered by a scikit-learn decision tree  
• Real-time explanations, testimonials, and trust cues to drive adoption  
• Feedback submission routed to Supabase for rapid iteration  
• Lightweight smoke tests to catch missing datasets or exports before deploy  

---

## Tech Stack 🛠️

• Python  
• Streamlit (UI) + streamlit-folium  
• Folium + Leaflet.js (Interactive mapping)  
• Supabase (Postgres, auth, and storage) via `supabase-py`  
• python-dotenv for local secrets management  
• scikit-learn DecisionTreeRegressor + Pandas preprocessing  
• Synthetic dataset generation pipeline  

---

## Getting Started ⚙️

1. Follow the full guide in `docs/SETUP.md` (Python env, Supabase keys, schema).
2. Run the data/model scripts once to refresh artifacts:
   ```
   python model/generate_dataset.py      # optional, synthetic data refresh
   python model/train_model.py          # trains tree + exports configs
   python model/explainability.py       # refreshes explanations.json
   ```
3. Launch the Streamlit UI:
   ```
   streamlit run frontend/app.py
   ```
4. (Optional) Verify everything with `python tests/smoke_tests.py`.

---

## Architecture 🧩

```
frontend/app.py        # Streamlit app with tabs for add/browse/predict/feedback
backend/supabase_*     # Reusable Supabase client + table helpers
model/                 # Data generation, training, predictor + artifacts
public/                # UCLA map assets for Folium overlay
docs/                  # Setup + structure docs 
tests/smoke_tests.py   # Quick CLI guardrails
```

Key flows:
- UI imports backend helpers instead of talking to Supabase directly, keeping secrets centralized.
- Model recommendations read `model/past_events.csv` at runtime for reproducibility.
- Event images default to Supabase Storage (`event-images` bucket) with a local `event_images/` fallback for debugging.

---

## Supabase Schema 🗄️

- `events`: stores organizer submissions, including `image_url`, `is_active`, and optional `close_reason`.
- `subscribers`: tracks simulated logins + preferred zones/diets for future notification triggers.
- `feedback`: captures contact form data from the Contact tab.
- Storage bucket `event-images`: public bucket for Streamlit uploads (inserting via service key).

Add Row-Level Security policies as needed; the local dev flow assumes a service-role key in `.env`.

---

## Testing ✅

Run `python tests/smoke_tests.py` to ensure required files exist, datasets are populated, exported trees are non-empty, and storage folders resolve before deploying to Streamlit Cloud or Hugging Face Spaces.

---

## Screenshots 📸

<img src="https://github.com/VidhiBhatt01/FoodLens/blob/main/public/foodlens.gif.gif">

<!--  
Add screenshots using:
![Screenshot](public/screenshot1.png)
-->

---

## Future Scope 🚀

- **Mobile companion app** for push alerts, GPS proximity, and one-tap event posting.
- **UCLA ecosystem integration** so events surface inside official campus apps and portals.
- **Predictor 2.0** with time-series data, richer explanations, and live calibration.
- **Impact dashboard** that quantifies pounds of food saved and highlights hotspots over time.
- **Smart check-ins** (QR/NFC) to compare predicted vs. actual attendance for continuous tuning.

---

<p align="center" style="color:gray; font-size:0.9rem;">
  Made with ❤️ by <b>Vidhi</b> (MS CS @ UCLA – Fall 2025)
</p>




