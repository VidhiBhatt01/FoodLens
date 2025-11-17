import pandas as pd
import numpy as np

np.random.seed(42)
N = 350

# Defining event attributes
event_types = ["club", "seminar", "fair", "career_fair"]
time_of_day = ["morning", "afternoon", "evening"]
buildings = ["north", "south", "central"]
day_of_week = ["mon", "tue", "wed", "thu", "fri"]

# Generating random event data
data = {
    "event_type": np.random.choice(event_types, N),
    "time_of_day": np.random.choice(time_of_day, N),
    "attendance": np.random.randint(10, 300, N),
    "building_zone": np.random.choice(buildings, N),
    "day": np.random.choice(day_of_week, N)
}

df = pd.DataFrame(data)

# Calculating surplus label based on event characteristics
def label_surplus(row):
    score = 0
    # Applying event type effects
    if row.event_type == "fair":
        score += 1.5
    if row.event_type == "career_fair":
        score += 1.2
    if row.event_type == "seminar":
        score -= 0.5
    # Applying time of day effects
    if row.time_of_day == "morning":
        score -= 0.5
    if row.time_of_day == "evening":
        score += 0.5
    # Applying attendance effects
    if row.attendance < 80:
        score += 1
    if row.attendance > 150:
        score -= 1
    # Applying building zone effects
    if row.building_zone == "north":
        score += 0.3
    if row.building_zone == "south":
        score -= 0.2
    # Applying weekly effects
    if row.day == "wed":
        score += 0.3
    if row.day in ["mon", "fri"]:
        score -= 0.2
    return 1 if score > 0.5 else 0

df["surplus"] = df.apply(label_surplus, axis=1)
df.to_csv("model/dataset.csv", index=False)
print("WROTE: model/dataset.csv")
