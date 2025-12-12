# 🚨 DoS Intrusion Detection System (IDS)

A machine-learning–based Intrusion Detection System designed to detect **DoS attacks, probing behavior, anomalies, and high-risk traffic** in real-time using the **NSL-KDD dataset**.

This project includes:
- ML-based traffic classification
- Real-time traffic simulation
- Parallel execution (simulator + predictor)
- Live network packet sniffing (Scapy + Npcap)
- Event-driven architecture
- Interactive Streamlit dashboard
- Desktop alert notifications

---

## 📌 Features

- 🔍 **Machine Learning Detection**
  - RandomForest classifier
  - Probability-based attack detection
-  **Parallel Traffic Simulation**
  - Multi-threaded packet generation
  - Controlled attack frequency
-  **Live Network Sniffer**
  - Captures real traffic using Scapy
- 🔔 **Event System**
  - Logger, alerter, mitigator observers
- 📊 **Streamlit Dashboard**
  - Real-time alerts and logs
-  **Desktop Notifications**
  - Popup alerts for detected attacks

---

## Project Architecture

DoS-IDS-Project/
│

├── main.py # Main control panel

├── main_real.py # Real attack replay

├── README.md

├── models/ # Trained ML model & scaler

│

├── src/

│ ├── predictor.py # ML prediction logic

│ ├── preprocess.py # Feature preprocessing

│ ├── simulator.py # Traffic simulator (parallel)

│ ├── sniffer.py # Live packet sniffer

│ │

│ ├── eventsystem/ # Event-driven architecture

│ │ ├── events.py

│ │ ├── logger.py

│ │ ├── alerter.py

│ │ ├── mitigator.py

│ │ └── observers/

│ │

│ └── dashboard/

│ └── app.py # Streamlit dashboard

│

├── logs/

│ └── alerts.log

│

└── attacks/ # Sample attack scenarios

---

## 🧠 Detection Types

| Type     | Description |
|--------|-------------|
| DoS     | Flooding & resource exhaustion |
| Probe   | Scanning & reconnaissance |
| Anomaly | Unusual traffic patterns |
| Normal  | Benign traffic |

---

## How to Run

### 1. Activate virtual environment
```bash
.venv\Scripts\activate
```
### 2. Start main control panel
```bash
python main.py
```
### 3. Run Dashboard (direct)
```bash
streamlit run src/dashboard/app.py
```
---

### Requirements
- Python 3.10+
- scikit-learn
- pandas
- numpy
- scapy
- streamlit
- plyer
- joblib
- Npcap (Windows)
