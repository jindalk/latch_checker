import subprocess
import datetime
import requests
import os

SSH_COMMAND = [
    "ssh",
    "-o", "ConnectTimeout=10",
    "latch-pod",
    "echo ok"
]

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message}, timeout=10)

def check_pod():
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    try:
        result = subprocess.run(SSH_COMMAND, capture_output=True, text=True, timeout=20)
        if result.returncode == 0 and "ok" in result.stdout:
            print(f"[{now}] Pod is RUNNING. Sending Telegram alert.")
            send_telegram_alert("Latch Bio pod is still running at 9:50 PM.")
        else:
            print(f"[{now}] Pod is NOT running.")
    except subprocess.TimeoutExpired:
        print(f"[{now}] Timeout. Pod likely not running.")
    except Exception as e:
        print(f"[{now}] SSH error: {e}")

if __name__ == "__main__":
    check_pod()
