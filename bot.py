import os
import time
import requests
from threading import Thread
from flask import Flask
import socketio

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    # ரெண்டர் வழங்கும் போர்ட்டை எடுக்கிறது
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

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
    except Exception as e:
        print(f"Token Error: {e}")
    return None

def start_bot_socket():
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to Groic Socket server successfully!")
        sio.emit('joinRoom', {'roomId': ROOM_ID})

    @sio.event
    def disconnect():
        print("Disconnected from Groic server.")

    while True:
        id_token = refresh_firebase_token()
        if id_token:
            print("Firebase Token refreshed, connecting to socket...")
            try:
                headers = {
                    "Authorization": id_token,
                    "x-app-version": "web",
                    "x-device-type": "web"
                }
                sio.connect('https://groic.in', headers=headers, transports=['websocket'])
                sio.wait()
            except Exception as e:
                print(f"Socket connection error: {e}")
        
        time.sleep(30)

if __name__ == "__main__":
    # Flask-ஐ தனி த்ரெட்டில் இயக்குதல்
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()

    # பாட் லாஜிக்கை பிரதானமாக இயக்குதல்
    start_bot_socket()
