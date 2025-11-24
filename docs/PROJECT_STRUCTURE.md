# FoodLens Project Structure

## Project Tree 

```
FoodLens/
├── backend/
│   ├── events.py
│   ├── subscribers.py
│   └── supabase_client.py
├── docs/
│   ├── ACADEMIC_ALIGNMENT.md
│   ├── PROJECT_STRUCTURE.md
│   └── SETUP.md
├── event_images/
│   └── (local debug uploads; Supabase is primary)
├── frontend/
│   └── app.py
├── model/
│   ├── dataset.csv
│   ├── explainability.py
│   ├── explanations.json
│   ├── generate_dataset.py
│   ├── past_events.csv
│   ├── predictor.py
│   ├── predictor_config.json
│   ├── predictor_tree.json
│   ├── train_model.py
│   └── tree.json
├── public/
│   ├── UCLA_MAP.pdf
│   └── UCLA_MAP.png
├── scripts/
│   ├── convert_map.py
│   └── print_tree.py
├── tests/
│   └── smoke_tests.py
├── README.md
└── requirements.txt
```

## Description of Key Components

### Root

- `README.md` – project overview, features, deployment notes, and roadmap.
- `requirements.txt` – unified Python dependencies (Streamlit UI, Supabase SDK, ML stack, pdf2image).

### Backend (`backend/`)

- `supabase_client.py` – loads `SUPABASE_URL`/`SUPABASE_KEY` from Streamlit secrets or `.env` and returns an authenticated client.
- `events.py` – CRUD helpers for the `events` table (fetch, insert, deactivate).
- `subscribers.py` – inserts opt-in notification preferences into the `subscribers` table.

### Frontend (`frontend/app.py`)

- Single Streamlit entry point with four tabs (Add Event, Browse Events, Food Surplus Predictor, Contact Us).
- Uses Supabase tables for persistent events, subscribers, and feedback plus Supabase Storage (`event-images` bucket) for media uploads.
- Renders Folium/Leaflet maps, Google Maps deep links, testimonials, and inline explanations from the predictor.

### Model (`model/`)

- `generate_dataset.py` – synthesizes realistic UCLA event data into `dataset.csv`.
- `train_model.py` – trains the interpretable decision-tree model and exports `predictor_tree.json` plus `predictor_config.json`.
- `predictor.py` – loads `past_events.csv`, builds a scikit-learn pipeline, and exposes `recommend()` for the UI.
- `explainability.py` – builds lightweight explanation artifacts saved to `explanations.json`.
- Data artifacts: `dataset.csv`, `past_events.csv`, `predictor_tree.json`, `tree.json`, `predictor_config.json`, and sample `explanations.json`.

### Public assets (`public/`)

- UCLA campus map assets consumed by Folium overlays (`UCLA_MAP.pdf` source, `UCLA_MAP.png` converted output).

### Scripts (`scripts/`)

- `convert_map.py` – helper to regenerate the PNG map (tries pdf2image then ImageMagick).
- `print_tree.py` – dumps the trained decision tree for inspection.

### Data storage (`event_images/`)

- Local fallback folder for debugging image uploads. Production flows push to Supabase Storage (`event-images` bucket).

### Documentation (`docs/`)

- `PROJECT_STRUCTURE.md` – this file.
- `SETUP.md` – environment setup, Supabase configuration, and run instructions.
- `ACADEMIC_ALIGNMENT.md` – coursework alignment notes.

### Testing (`tests/`)

- `smoke_tests.py` – CLI smoke tests that verify key files exist, datasets are populated, exported trees are readable, and storage directories resolve.
