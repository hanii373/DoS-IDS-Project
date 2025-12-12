import time
import random
from concurrent.futures import ThreadPoolExecutor

from predictor import predict_single, feature_template



# CONFIGURATION
SIMULATION_DURATION = 3      # seconds
MAX_ATTACKS = 5              # max detected attacks
PACKET_INTERVAL = 0.5        # seconds between packets
WORKERS = 2                  # parallel workers

def generate_packet():
    """
    Generate a synthetic NSL-KDD–compatible packet.
    """
    packet = {feature: 0 for feature in feature_template}

    # Normal traffic
    packet["src_bytes"] = random.randint(0, 3000)
    packet["dst_bytes"] = random.randint(0, 3000)
    packet["count"] = random.randint(1, 40)
    packet["srv_count"] = random.randint(1, 50)

    if random.random() < 0.30:
        packet["src_bytes"] = random.randint(3500, 7000)
        packet["dst_bytes"] = random.randint(0, 5)
        packet["count"] = random.randint(60, 200)

    if random.random() < 0.20:
        packet["dst_bytes"] = random.randint(0, 10)
        packet["count"] = random.randint(40, 150)

    if random.random() < 0.10:
        packet["src_bytes"] = random.randint(4000, 8000)
        packet["dst_bytes"] = random.randint(0, 2)

    return packet

def run_simulator_parallel(duration=5, max_attacks=5):
    """
    Runs parallel traffic simulation for a fixed duration
    and limits number of attacks.
    """
    import time
    import random
    from concurrent.futures import ThreadPoolExecutor

    start_time = time.time()
    attack_count = 0

    print("🚀 Parallel Simulator Started")

    def generate_packet():
        packet = {feature: 0 for feature in feature_template}

        packet["src_bytes"] = random.randint(0, 1500)
        packet["dst_bytes"] = random.randint(0, 1500)
        packet["count"] = random.randint(1, 40)
        packet["srv_count"] = random.randint(1, 50)

        nonlocal attack_count
        if attack_count < max_attacks and random.random() < 0.25:
            packet["src_bytes"] = random.randint(4000, 7000)
            packet["dst_bytes"] = random.randint(0, 5)
            packet["count"] = random.randint(80, 200)
            attack_count += 1

        return packet

    def callback(future):
        prob, attack_type = future.result()
        print(f"[Parallel] Prob={prob:.4f} | Type={attack_type}")


    with ThreadPoolExecutor(max_workers=4) as executor:
        while time.time() - start_time < duration:
            pkt = generate_packet()
            future = executor.submit(predict_single, pkt)
            future.add_done_callback(callback)
            time.sleep(0.4)

    print("✔ Simulator finished.")
