import json
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

# Loading and training predictor model from past events
def load_predictor():
    df = pd.read_csv("model/past_events.csv")
    X = df[["building","zone","event_type","day","time","rsvps"]]
    y_attendance = df["expected_attendance"]

    categorical = ["building","zone","event_type","day","time"]
    numerical = ["rsvps"]

    preprocess = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numerical),
        ]
    )

    model = Pipeline(steps=[
        ("preprocess", preprocess),
        ("tree", DecisionTreeRegressor(max_depth=5, random_state=42))
    ])
    model.fit(X, y_attendance)
    return model

# Generating food recommendation based on event details
def recommend(building, zone, event_type, day, time, rsvps, planned_food):
    model = load_predictor()

    # Preparing input data for prediction
    row = pd.DataFrame([{
        "building": building,
        "zone": zone,
        "event_type": event_type,
        "day": day,
        "time": time,
        "rsvps": rsvps
    }])
    pred_att = model.predict(row)[0]

    # Loading configuration parameters
    with open("model/predictor_config.json") as f:
        cfg = json.load(f)

    # Calculating recommended food quantity
    reco_food = max(rsvps, int(pred_att + cfg["food_buffer"]))
    reduction = planned_food - reco_food

    # Building explanation text
    explanation = [
        f"Predicted attendance: ~{int(pred_att)} based on similar past events.",
        f"RSVPs: {rsvps}. Planned food: {planned_food}.",
        f"Model recommends ordering {reco_food} to cover buffer while reducing surplus risk."
    ]

    return {
        "predicted_attendance": int(pred_att),
        "recommended_food": int(reco_food),
        "reduction": int(reduction),
        "explanation": explanation
    }

if __name__ == "__main__":
    # Running demo prediction
    demo = recommend(
        building="Boelter Hall",
        zone="north",
        event_type="club",
        day="wed",
        time="18:00",
        rsvps=150,
        planned_food=160
    )
    print(demo)
