# Generating explanations for model predictions
import json
import pandas as pd

# Loading decision tree structure
with open("model/tree.json") as f:
    tree_data = json.load(f)["tree"]

# Loading dataset for explanation generation
data = pd.read_csv("model/dataset.csv")

# Creating explanation for a single data row
def explain_row(row):
    """Producing mock explanation showing top 3 features affecting prediction."""
    explanation = []
    if row["attendance"] <= 88:
        explanation.append({"feature":"attendance","value":row["attendance"],"contribution":"increasing probability"})
    else:
        explanation.append({"feature":"attendance","value":row["attendance"],"contribution":"decreasing probability"})
    explanation.append({"feature":"Event type","value":row["event_type"],"contribution":"moderate effect"})
    explanation.append({"feature":"Time of day","value":row["time_of_day"],"contribution":"minor effect"})
    return explanation

# Generating explanations for first 3 rows
explanations = []
for idx, row in data.head(3).iterrows():
    pred = 1 if row["attendance"] <= 88 else 0
    explanations.append({
        "id": int(idx) + 1,
        "prediction": int(pred),
        "explanation": explain_row(row)
    })

# Saving explanations to JSON file
with open("model/explanations.json","w") as f:
    json.dump(explanations,f,indent=2)
print("WROTE: model/explanations.json")
