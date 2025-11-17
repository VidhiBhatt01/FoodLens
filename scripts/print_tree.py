import json

with open("model/tree.json") as f:
    data = json.load(f)

print(data["tree"])
