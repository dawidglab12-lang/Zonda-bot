import os, threading
from flask import Flask
import subprocess

def run_bot():
    # uruchamia zonda_autotrader.py w osobnym procesie
    subprocess.call(["python", "zonda_autotrader.py"])

t = threading.Thread(target=run_bot, daemon=True)
t.start()

app = Flask(__name__)

@app.get("/")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
