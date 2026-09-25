import time
import os
from parser import parse_line, init_stats
from detector import detect_suspicious, detect_bots

def stream_logs(socketio):
    # ✅ FIX: Go to project ROOT (one level up from backend)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(BASE_DIR)

    # ✅ Use ROOT logs folder
    LOG_FILE = os.path.join(ROOT_DIR, "logs", "app.log")

    print("📡 Reading from:", LOG_FILE)

    stats = init_stats()

    # ✅ wait until file exists
    while not os.path.exists(LOG_FILE):
        print("⏳ Waiting for logs/app.log...")
        time.sleep(1)

    print("✅ Reading existing logs...")

    with open(LOG_FILE, "r") as file:

        # ✅ STEP 1: READ FULL FILE
        for line in file:
            try:
                stats = parse_line(line, stats)
            except Exception as e:
                print("❌ Error parsing old log:", e)

        print("📊 Initial data loaded")

        # ✅ Send initial data
        data = {
            "failed_logins": stats["failed_logins"],
            "success_logins": stats["success_logins"],
            "bot_detected": stats["bot_detected"],
            "requests_per_ip": dict(stats["requests_per_ip"]),
            "suspicious_ips": detect_suspicious(stats["requests_per_ip"]),
            "bots": detect_bots(stats["user_agents"])
        }

        print("📤 Initial data sent:", data)
        socketio.emit("update", data)

        # ✅ STEP 2: LIVE STREAM
        file.seek(0, 2)

        print("📡 Live streaming started...")

        while True:
            where = file.tell()
            line = file.readline()

            if not line:
                time.sleep(0.5)
                file.seek(where)
                continue

            print("📥 New log:", line.strip())

            try:
                stats = parse_line(line, stats)

                data = {
                    "failed_logins": stats["failed_logins"],
                    "success_logins": stats["success_logins"],
                    "bot_detected": stats["bot_detected"],
                    "requests_per_ip": dict(stats["requests_per_ip"]),
                    "suspicious_ips": detect_suspicious(stats["requests_per_ip"]),
                    "bots": detect_bots(stats["user_agents"])
                }

                print("📤 Sending update:", data)
                socketio.emit("update", data)

            except Exception as e:
                print("❌ Error processing log:", e)