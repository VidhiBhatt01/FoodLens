# Setup Guide



## 1. Clone the repository
```
git clone <repo-url>

cd FoodLens
```


## 2. Create a virtual environment
```
python -m venv .venv  

source .venv/bin/activate   (Mac/Linux)  

.venv\Scripts\activate      (Windows)
```


## 3. Install dependencies
```
pip install -r requirements.txt
```


## 4. Generate synthetic dataset
```
python model/generate_dataset.py
```


## 5. Train interpretable model
```
python model/train_model.py
```


## 6. Export explanation mappings
```
python model/explainability.py
```


## 7. Run the web application
```
streamlit run frontend/app.py
```


## 8. Event images (optional)
```
Uploaded event images are stored in event_images/.
```


## 9. Basic tests
```
python tests/smoke_tests.py
```
