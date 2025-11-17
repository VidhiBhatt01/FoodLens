import pandas as pd
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.tree import export_text
import json

# Loading past events dataset
df = pd.read_csv("model/past_events.csv")

# Preparing features and target for attendance prediction
X = df[["building","zone","event_type","day","time","rsvps"]]
y_attendance = df["expected_attendance"]

# Defining categorical and numerical features
categorical = ["building","zone","event_type","day","time"]
numerical = ["rsvps"]

# Creating preprocessing pipeline with one-hot encoding
preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numerical),
    ]
)

# Building attendance prediction model
attendance_model = Pipeline(steps=[
    ("preprocess", preprocess),
    ("tree", DecisionTreeRegressor(max_depth=5, random_state=42))
])

# Training the model
attendance_model.fit(X, y_attendance)

# Evaluating model performance on training data
pred_att = attendance_model.predict(X)
# Deriving surplus classification from predicted attendance
food_ordered = df["rsvps"] * 1.1
y_surplus = (food_ordered > df["expected_attendance"] + 15).astype(int)
pred_surplus = (food_ordered > pred_att + 15).astype(int)
acc = accuracy_score(y_surplus, pred_surplus)
print("Surplus classification accuracy:", round(acc, 3))

# Exporting decision tree as readable text
tree_text = export_text(
    attendance_model.named_steps["tree"],
    feature_names=list(attendance_model.named_steps["preprocess"].get_feature_names_out()),
    max_depth=5
)

# Saving tree structure to JSON
with open("model/predictor_tree.json","w") as f:
    json.dump({"tree": tree_text}, f, indent=2)
print("WROTE: model/predictor_tree.json")

# Saving predictor configuration
config = {"food_buffer": 15, "extra_percent": 0.1}
with open("model/predictor_config.json","w") as f:
    json.dump(config,f,indent=2)
print("WROTE: model/predictor_config.json")
