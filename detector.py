from collections import defaultdict
from sklearn.ensemble import IsolationForest
import numpy as np

def detect_suspicious(requests_per_ip):
    suspicious = []

    # Rule-based detection
    for ip, count in requests_per_ip.items():
        if count > 10:
            suspicious.append(ip)

    # ML-based anomaly detection
    if len(requests_per_ip) > 3:
        data = np.array(list(requests_per_ip.values())).reshape(-1, 1)
        model = IsolationForest(contamination=0.3)
        preds = model.fit_predict(data)

        for i, (ip, _) in enumerate(requests_per_ip.items()):
            if preds[i] == -1:
                suspicious.append(ip)

    return list(set(suspicious))


def detect_bots(user_agents):
    bots = []
    for ip, agent in user_agents.items():
        if "python" in agent.lower() or "bot" in agent.lower():
            bots.append(ip)
    return bots