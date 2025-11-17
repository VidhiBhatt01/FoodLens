<h1 align="center">FoodLens 🍕🔍</h1>
<!-- Banner -->
<p align="center">
  <img src="https://img.shields.io/badge/FoodLens-UCLA%20Free%20Food%20Finder-005587?style=for-the-badge&logo=leaflet&logoColor=white" alt="FoodLens Banner">
</p>

<p align="center">
  <i>Reducing food waste. Empowering students. Built with ethical and interpretable AI.</i>
</p>

<!-- Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
  <img src="https://img.shields.io/badge/Streamlit-Deployable-FF4B4B.svg">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB.svg">
  <img src="https://img.shields.io/badge/Model-Interpretable%20ML-blue.svg">
  <img src="https://img.shields.io/badge/Status-Active-success">
</p>

FoodLens is a campus-wide platform to reduce food waste by connecting surplus event food with students in real time.  
Designed with transparency, safety, and ethical AI principles inspired by UCLA CS 269.

---

## Overview 🌿

FoodLens enables event organizers to quickly post surplus food availability on campus, helping students find free food while reducing waste.  
Students can browse active events, customize notification preferences, and view event locations on an interactive UCLA map.

An interpretable machine-learning predictor estimates expected attendance to help organizers avoid over-ordering, maintaining transparency and fairness throughout the system.

---

## Features ✨

• Add a free-food event with details and optional image upload  
• Browse active events through clean, collapsible dropdowns  
• View event locations on an interactive map + Google Maps redirection  
• Customizable email notifications for subscribed users  
• Field-level validated email input for stronger data hygiene  
• Image support for event posts and simulated email notifications  
• Transparent attendance predictor using an interpretable decision tree  
• Always-visible testimonials for trust and usability credibility  
• Feedback submission page for student/community engagement  
• Footer branding for project identity  

---

## Tech Stack 🛠️

• Python  
• Streamlit (UI)  
• Folium + Leaflet.js (Interactive mapping)  
• scikit-learn (Model)  
• Pandas (Data)  
• Custom rule-based + interpretable decision tree model  
• Synthetic dataset generation pipeline  

---

## Screenshots 📸

Coming soon.

<!--  
Add screenshots using:
![Screenshot](public/screenshot1.png)
-->

---

## Future Scope 🚀

FoodLens is designed to be lightweight today but highly extensible. Possible future enhancements include:

### Mobile App Integration 📱
A dedicated iOS/Android app allowing:
• Push notifications for nearby free food  
• Real-time GPS proximity matching  
• Quick event posting with camera integration  

### UCLA Campus App Integration 🎓
Embedding FoodLens directly into the official UCLA mobile app to:
• Serve incoming notifications based on building geofences  
• Display food events alongside MyUCLA schedules  
• Provide analytics to student groups for budgeting food orders  

### Smart Food Prediction 2.0 🤖
Enhance the ML pipeline with:
• Time-series modeling on event participation  
• Real historical UCLA event data (with permission)  
• Model explanations using SHAP or rule extraction  

### Community Impact Dashboard 📊
Analytics for UCLA sustainability offices:
• Estimated pounds of food saved  
• Waste reduction over time  
• Building-level insights for planners  

### NFC / QR Code Check-ins 🎫
Optional attendee check-ins to measure accuracy between predicted vs. actual attendance.

---

<p align="center" style="color:gray; font-size:0.9rem;">
  Made with ❤️ by <b>Vidhi</b> (MS CS @ UCLA – Fall 2025)
</p>

