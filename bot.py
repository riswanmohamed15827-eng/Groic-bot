import os
import time
import requests
from threading import Thread
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

API_KEY = "AIzaSyAz51581sbr0pX9Q5uQwdTnNMA80"
REFRESH_TOKEN = "AMf-vByw8FAmxA_6KlZW4QaAk95y2eAlwQctqs6Xm17WLhbBH18CG-pn8pSGIWytVm--_SxTByiHjfISm_t5EX4ruRO-YyJ2uUYTiAHrUXgvVftoO_RneW8SGignHtpxJPAWqg02GZ1EA3el6wGuyDDQRS3AJd0QYc9FyVyoEW8ok3raFEG7Zf1nSo7DKrtWhFqcxPaIILPsja1jZfqLPIB4QV3my1VXy-eN6SlO1XvBpyLDbAa9HaebR4ZE4YMP-471Gy02G9cqaIzjDEe65hobYXdn1ip5gLslVPtuxujbBub1ud4T7_mmmtDBTNeJykQq-BfDGM6pXAo_n7vXfqGicUKoDVe5wP4R3MwE8qB3HdCSUtRS9-jU6XsAtaZBLy8dqXz4VuHvFJYptOmA7Kxt-G-h7jliRLo9mwh_pVLvTGAdNJPvLf8"
ROOM_ID = "37uqc814uu"

def refresh_firebase_token():
    url = f"https://securetoken.googleapis.com/v1/token?key={API_KEY}"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("id_token")
        else:
            print(f"Token Refresh Error: {response.text}")
    except Exception as e:
        print(f"Exception during token refresh: {e}")
    return None

def bot_loop():
    print(f"Groic bot started for Room ID: {ROOM_ID}")
    while True:
        id_token = refresh_firebase_token()
        if id_token:
            print("Successfully authenticated with Firebase and got ID Token!")
        else:
            print("Authentication failed, retrying in next cycle...")
        time.sleep(30)

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot_loop()
