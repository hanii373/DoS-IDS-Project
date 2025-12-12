from concurrent.futures import ThreadPoolExecutor, as_completed
from predictor import predict_single  

EXECUTOR = ThreadPoolExecutor(max_workers=4)


def predict_async(feature_dict):
    """
    Submit a single prediction job to the thread pool.
    Returns a Future object.
    """
    return EXECUTOR.submit(predict_single, feature_dict)


def predict_batch(list_of_packets):
    """
    Predict many packets in parallel.
    Returns list of results.
    """
    futures = [EXECUTOR.submit(predict_single, pkt) for pkt in list_of_packets]
    results = []

    for f in as_completed(futures):
        results.append(f.result())

    return results
