# 🪖 Helmet & Road Safety Compliance 🚦  
![Made with YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-blue?logo=python&logoColor=white)
![Hackathon](https://img.shields.io/badge/Hackathon-Ignithon-orange)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)

> **AI-powered helmet detection system for promoting road safety and reducing traffic fatalities.**  

---

## 📌 Problem Statement  
Road traffic accidents are a **leading cause of injuries and deaths** worldwide.  
A major risk factor: **riders not wearing helmets**.  

- 🚔 Manual enforcement = **time-consuming** and **resource-heavy**  
- ⚠️ Lack of a **scalable & automated solution** today  

This project provides an **AI-based helmet compliance detection system** that supports authorities, raises awareness, and helps **prevent accidents**.  

---

## ✨ Features  
✅ Detects **motorbike riders** in real-time  
✅ Flags **helmet compliance** (Safe ✅ / Unsafe ❌)  
✅ Live statistics of **helmet vs non-helmet riders**  
✅ Outputs **annotated frames** with colored bounding boxes  
✅ Scalable for **traffic monitoring and smart city use-cases**  

---

## ⚙️ How It Works  
1. **Input**: Video stream / webcam / uploaded footage  
2. **Detection**: YOLOv8 detects persons, motorcycles, helmets  
3. **Logic**: If `person` overlaps with `motorcycle` → check helmet presence  
4. **Classification**:  
   - 🟩 **Helmet** → Safe  
   - 🟥 **No Helmet** → Unsafe  
5. **Output**: Annotated frames + Live count stats  

---

## 🏗️ Tech Stack  
- **AI/ML**: [YOLOv8](https://github.com/ultralytics/ultralytics), PyTorch  
- **Computer Vision**: OpenCV  
- **Backend**: Flask / FastAPI *(planned for deployment)*  
- **Frontend**: Streamlit / React *(dashboard & uploads)*  
- **Visualization**: Plotly / Chart.js *(statistics)*  
- **Database**: SQLite / Firebase *(storage)*  

---

## 📂 Project Structure  

 ── objecthelmot.py # Main detection script
├── best.pt # Custom trained helmet detection model
├── yolov8n.pt # Pretrained COCO YOLOv8 model
├── README.md # Documentation
└── /data # (optional) Dataset / sample video

## ▶️ Run Detection

python objecthelmot.py
Opens webcam / video feed by default

Press q to quit

## 📊 Example Output
sql
Copy
Edit
With Helmet: 5
Without Helmet: 2
🟩 Rider with helmet → Green Box (Safe)

🟥 Rider without helmet → Red Box (Unsafe)




## 🌐 United Nations SDGs Fulfilled

This project aligns with the United Nations Sustainable Development Goals (SDGs):

SDG 3: Good Health & Well-Being 🏥

Reduces risk of head injuries and fatalities by promoting helmet usage.

Encourages safer roads and healthier communities.

SDG 11: Sustainable Cities & Communities 🏙️

Supports smart city initiatives through automated traffic monitoring.

Enhances road safety compliance at scale.

## 🌍 Impact

Promotes road safety awareness

Helps law enforcement with automated compliance checks

Boosts smart city surveillance initiatives

## 👨‍💻 Team — Big Three

Soham Dutta (22052064)

Paurab De (22051703)

Sayandeep Kanrar (22053357)
