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

├── main.py                # Main control panel (menu-based launcher)

├── main_real.py           # Real-traffic simulation runner (JSON scenarios)

├── requirements.txt

├── README.md

├── .gitignore

│

├── models/

│   ├── baseline_model.joblib   # Trained Random Forest model

│   └── scaler.pkl              # Scaler for feature normalization

│

├── data/                       # (Not pushed to GitHub – large datasets)

│

├── logs/

│   └── alerts.log              # Attack logs used by dashboard

│

├── attacks/

│   ├── sample_dos.json

│   ├── sample_probe.json

│   ├── sample_anomaly.json

│   └── scenario_mixed.json

│

├── src/

│   ├── predictor.py            # Core ML prediction logic

│   ├── preprocess.py           # Feature preprocessing (runtime)

│   ├── simulator.py            # Traffic simulator (parallel + limited duration)

│   ├── sniffer.py               # Real network packet sniffer (Scapy + Npcap)

│   │

│   ├── dashboard/

│   │   └── app.py               # Streamlit dashboard UI

│   │

│   └── eventsystem/

│       ├── events.py            # EventManager (publish/subscribe)

│       ├── observer.py          # Base Observer class

│       ├── logger.py            # AttackLogger (writes logs)

│       ├── alerter.py            # Popup alerts (Plyer)

│       ├── mitigator.py          # Mitigation logic (placeholder / basic)

│       ├── observer_probe.py     # Probe-specific observer

│       ├── observer_anomaly.py   # Anomaly-specific observer

│       └── observer_highrisk.py  # High-risk attack observer

│

└── .venv/                       # Virtual environment

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
