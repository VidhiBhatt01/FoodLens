import os
import pandas as pd

def check_file_exists(path):
    if not os.path.exists(path):
        raise AssertionError(f"Missing required file: {path}")
    print(f"✔ Found: {path}")

def check_dataset():
    df = pd.read_csv("model/data.csv")
    if len(df) < 10:
        raise AssertionError("Dataset has fewer than 10 rows.")
    print(f"✔ Dataset OK ({len(df)} rows)")

def check_model_export():
    data = open("model/tree.json", "r").read().strip()
    if data == "" or data is None:
        raise AssertionError("tree.json is empty or unreadable.")
    print("✔ Model export OK (tree.json)")

def check_frontend():
    check_file_exists("frontend/app.py")

def check_images_folder():
    os.makedirs("event_images", exist_ok=True)
    print("✔ event_images folder OK")

def run_all():
    print("\nRunning FoodLens Smoke Tests\n")
    check_file_exists("requirements.txt")
    check_file_exists("model/generate_dataset.py")
    check_file_exists("model/train_model.py")
    check_file_exists("model/explainability.py")
    check_file_exists("model/predictor.py")
    check_dataset()
    check_model_export()
    check_frontend()
    check_images_folder()
    print("\nALL SMOKE TESTS PASSED ✔\n")

if __name__ == "__main__":
    run_all()

