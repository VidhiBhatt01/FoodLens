# FoodLens Project Structure

## Project Tree

```
FoodLens/
├── docs/
│   ├── PROJECT_STRUCTURE.md
│   └── SETUP.md
├── event_images/
│   └── (uploaded event images)
├── frontend/
│   └── app.py
├── model/
│   ├── dataset.csv
│   ├── explainability.py
│   ├── explanations.json
│   ├── generate_dataset.py
│   ├── past_events.csv
│   ├── predictor_config.json
│   ├── predictor.py
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

### Root Level Files

README.md  
• Project overview and feature documentation  
• Tech stack information  
• Screenshots section placeholder  

requirements.txt  
• Python package dependencies  
• Includes pandas, scikit-learn, streamlit, folium, etc.  

### Frontend

frontend/app.py  
• Main Streamlit user interface  
• Four tabs: Add Event, Browse Events, Food Surplus Predictor, Contact Us  
• Interactive map with Folium for event locations  
• Event posting with image upload support  
• Email notification preferences with validation  
• Interpretable predictor integration  
• User testimonials display  
• Feedback submission form  

### Model

model/generate_dataset.py  
• Generating synthetic event dataset  
• Creating realistic event data with surplus labels  
• Outputs dataset.csv with ~350 rows  

model/train_model.py  
• Training DecisionTreeRegressor for attendance prediction  
• Preprocessing categorical features with OneHotEncoder  
• Evaluating surplus classification accuracy  
• Exporting tree structure to predictor_tree.json  
• Saving predictor configuration to predictor_config.json  

model/predictor.py  
• Loading and training predictor model  
• Generating food recommendations based on event details  
• Calculating recommended food quantities  
• Providing interpretable explanations  

model/explainability.py  
• Generating explanations for model predictions  
• Creating feature contribution mappings  
• Exporting explanations to JSON format  

model/dataset.csv  
• Synthetic training dataset  
• Contains event features and surplus labels  

model/past_events.csv  
• Historical event data for model training  
• Includes building, zone, event type, attendance data  

model/tree.json  
• Exported decision tree structure  
• Human-readable tree representation  

model/predictor_tree.json  
• Trained predictor tree structure  
• Used for interpretability  

model/predictor_config.json  
• Configuration parameters for predictor  
• Contains food buffer and extra percentage settings  

model/explanations.json  
• Pre-generated explanations for sample events  
• Used for demonstration purposes  

### Scripts

scripts/convert_map.py  
• Converting PDF map to PNG format  
• Attempting pdf2image first, falling back to ImageMagick  
• Creating public/UCLA_MAP.png for map overlay  

scripts/print_tree.py  
• Utility script for viewing decision tree  

### Public Assets

public/  
• UCLA_MAP.pdf: Source PDF map of UCLA campus  
• UCLA_MAP.png: Converted PNG map for display  

### Data Storage

event_images/  
• Directory for uploaded event images  
• Created automatically when images are uploaded  
• Images stored with original filenames  

### Documentation

docs/PROJECT_STRUCTURE.md  
• This file: Project structure documentation  

docs/SETUP.md  
• Setup and installation instructions  
• Step-by-step guide for running the application  

### Testing

tests/smoke_tests.py  
• Basic smoke tests for project health  
• Checking file existence and dataset validity  
• Verifying model exports and frontend files  
• Ensuring required directories exist