from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import threading
import logging
import os
from streamer import stream_logs

app = Flask(__name__)
CORS(app)

# ✅ Socket setup (Windows safe)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    logger=True,
    engineio_logger=True
)

# ✅ FIX: Go to project ROOT
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

# ✅ Use ROOT logs folder
LOG_DIR = os.path.join(ROOT_DIR, "logs")

# create if not exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

print("📁 Writing logs to:", LOG_FILE)

# ✅ Logging setup
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ✅ Force file creation
logging.info("🚀 Server started")

# ✅ Flush logs immediately
def flush_logs():
    for handler in logging.getLogger().handlers:
        handler.flush()

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return "✅ Real-time Security Dashboard Running"

@app.route("/login")
def login_route():
    print("👉 /login hit")
    logging.info("LOGIN_SUCCESS user=test ip=127.0.0.1")
    flush_logs()
    return "Logged in"

@app.route("/fail")
def fail_route():
    print("👉 /fail hit")
    logging.info("LOGIN_FAIL user=admin ip=127.0.0.1")
    flush_logs()
    return "Failed login simulated"

@app.route("/bot")
def bot_route():
    print("👉 /bot hit")
    logging.info("BOT_DETECTED ip=127.0.0.1 agent=python-requests")
    flush_logs()
    return "Bot simulated"

# ---------------- STREAM THREAD ---------------- #

def start_stream():
    print("📡 Starting log stream thread...")
    stream_logs(socketio)

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    print("🚀 Starting Flask Server...")

    thread = threading.Thread(
        target=start_stream,
        daemon=True
    )
    thread.start()

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )