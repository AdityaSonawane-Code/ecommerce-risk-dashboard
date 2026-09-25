import re
from collections import defaultdict

def parse_line(line, stats):
    # Login events
    if "LOGIN_FAIL" in line:
        stats["failed_logins"] += 1

    if "LOGIN_SUCCESS" in line:
        stats["success_logins"] += 1

    # Bot detection
    if "BOT_DETECTED" in line:
        stats["bot_detected"] += 1

    # E-commerce actions
    if "CHECKOUT" in line:
        stats["checkouts"] += 1

    if "ADD_TO_CART" in line:
        stats["cart_adds"] += 1

    # Extract IP
    ip_match = re.search(r'ip=([\d\.]+)', line)
    agent_match = re.search(r'agent=([^\s]+)', line)

    if ip_match:
        ip = ip_match.group(1)
        stats["requests_per_ip"][ip] += 1

        if agent_match:
            stats["user_agents"][ip] = agent_match.group(1)

    return stats


def init_stats():
    return {
        "failed_logins": 0,
        "success_logins": 0,
        "bot_detected": 0,
        "checkouts": 0,
        "cart_adds": 0,
        "requests_per_ip": defaultdict(int),
        "user_agents": {}
    }