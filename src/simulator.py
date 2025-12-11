# simulator.py
# Generates synthetic NSL-KDD–compatible traffic and feeds it into predictor.py

import time
import random
import numpy as np
import pandas as pd
from predictor import predict_single, feature_template

print("Simulator running...")


# ==============================================================
#  FUNCTION: Generate NSL-KDD-Compatible Feature Vector
# ==============================================================

def generate_packet():
    """
    Create a full feature vector matching the 122 features expected by the model.
    We fill all columns with zeros, then override some meaningful fields.
    """
    # Create full feature dictionary with all 122 columns
    packet = {feature: 0 for feature in feature_template}

    # ----------------------------
    # NORMAL TRAFFIC SIMULATION
    # ----------------------------
    packet["src_bytes"] = random.randint(0, 3000)
    packet["dst_bytes"] = random.randint(0, 3000)
    packet["count"] = random.randint(1, 40)
    packet["srv_count"] = random.randint(1, 50)
    packet["dst_host_count"] = random.randint(1, 255)

    # ---------------------------------------------------
    # 20% CHANCE: SIMULATE A DoS ATTACK
    # ---------------------------------------------------
    if random.random() < 0.80:
        packet["src_bytes"] = random.randint(3000, 6000)
        packet["dst_bytes"] = random.randint(0, 5)
        packet["count"] = random.randint(50, 200)  # rapid packets

    # ---------------------------------------------------
    # 10% CHANCE: SIMULATE PROBE / SCANNING BEHAVIOR
    # ---------------------------------------------------
    if random.random() < 0.50:
        packet["dst_bytes"] = random.randint(0, 10)
        packet["count"] = random.randint(40, 150)

    # ---------------------------------------------------
    # 10% CHANCE: SIMULATE ANOMALY
    # ---------------------------------------------------
    if random.random() < 0.10:
        packet["src_bytes"] = random.randint(3500, 7000)
        packet["dst_bytes"] = random.randint(0, 2)

    return packet


# ==============================================================
#  MAIN LOOP — Real-Time Traffic Generation
# ==============================================================

if __name__ == "__main__":
    while True:
        sample = generate_packet()

        # Event-driven detection happens inside predict_single()
        result = predict_single(sample)
        print("Packet prob:", result["prob"])


        # Adjust speed of traffic
        time.sleep(0.5)   # 2 packets per second
