import time
import random
import threading
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(BASE_DIR, "logs", "app.log")

ips = ["192.168.1.1", "192.168.1.2", "10.0.0.5", "172.16.0.3"]
users = ["aditya", "rahul", "guest", "admin"]
products = ["laptop", "phone", "shoes", "watch"]

def write_log(event):
    with open(log_path, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {event}\n")


def simulate_user():
    while True:
        ip = random.choice(ips)
        user = random.choice(users)

        action = random.choices(
            ["normal", "attack", "bot"],
            weights=[70, 20, 10]
        )[0]

        if action == "normal":
            event = random.choice([
                f"LOGIN_SUCCESS user={user} ip={ip}",
                f"VIEW_PRODUCT product={random.choice(products)} ip={ip}",
                f"ADD_TO_CART product={random.choice(products)} ip={ip}",
                f"CHECKOUT user={user} ip={ip}",
                f"REQUEST path=/api/products ip={ip}"
            ])
            write_log(event)

        elif action == "attack":
            # brute force burst
            for _ in range(random.randint(3, 8)):
                write_log(f"LOGIN_FAIL user=admin ip={ip}")
                time.sleep(0.1)

        elif action == "bot":
            write_log(f"BOT_DETECTED ip={ip} agent=python-requests")

        time.sleep(random.uniform(0.2, 1))


# 🔥 simulate multiple concurrent users
threads = []
for _ in range(5):  # 5 concurrent users
    t = threading.Thread(target=simulate_user)
    t.daemon = True
    t.start()
    threads.append(t)

# keep main alive
while True:
    time.sleep(1)