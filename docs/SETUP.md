# Setup Guide

## 0. Prerequisites

- Python 3.10+ and `pip`
- Supabase project (free tier works) with:
  - Tables: `events`, `subscribers`, `feedback`
  - Storage bucket: `event-images` (public read)
- Optional: ImageMagick if pdf2image is not available (for `scripts/convert_map.py`)

## 1. Clone the repository

```
git clone <repo-url>
cd FoodLens
```

## 2. Create & activate a virtual environment

```
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

## 3. Install dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Supabase credentials

FoodLens auto-loads credentials from Streamlit secrets (cloud deploy) or `.env` (local).

Create a `.env` file in the repo root:

```
SUPABASE_URL=<your-project-url>
SUPABASE_KEY=<your-service-role-or-anon-key>
```

> Never commit `.env` or keys. For Streamlit Cloud, add the same keys under `Secrets`.

## 5. Provision Supabase resources

Create the following tables (SQL types shown for reference):

- `events`: `id uuid default uuid_generate_v4() primary key`, `building text`, `zone text`, `event_type text`, `diet text`, `food_desc text`, `collect_mode text`, `collect_until_time text`, `image_url text`, `is_active boolean default true`, `close_reason text`, `created_at timestamptz default now()`.
- `subscribers`: `id uuid primary key default uuid_generate_v4()`, `username text`, `email text`, `zones text[]`, `diets text[]`, `created_at timestamptz default now()`.
- `feedback`: `id uuid primary key default uuid_generate_v4()`, `name text`, `email text`, `message text`, `created_at timestamptz default now()`.

Storage: create a bucket named `event-images`, mark it public, and (optionally) add an RLS policy allowing inserts from the service role key.

## 6. Prepare model artifacts

Run the data + model pipeline once (rerun whenever you refresh the training data):

```
python model/generate_dataset.py      # Optional synthetic data refresh
python model/train_model.py          # Trains the interpretable tree + exports configs
python model/explainability.py       # Updates explanations.json for demos
```

The predictor also reads `model/past_events.csv`; update it if you collect new historical data.

## 7. Run the Streamlit app

```
streamlit run frontend/app.py
```

Uploads go to Supabase Storage. During local debugging you can still inspect `event_images/`, but cloud deployments exclusively use Supabase.

## 8. Run smoke tests (optional)

```
python tests/smoke_tests.py
```

These checks validate required files, datasets, and exported model artifacts before deployment.
