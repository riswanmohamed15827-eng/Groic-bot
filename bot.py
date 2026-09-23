import os
import time
from threading import Thread
from flask import Flask
import socketio

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

ROOM_ID = "37uqc814uu"

def start_bot_socket():
    print("Bot socket initialization started...", flush=True)
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to Groic Socket server successfully!", flush=True)
        sio.emit('joinRoom', {'roomId': ROOM_ID})

    @sio.event
    def disconnect():
        print("Disconnected from Groic server.", flush=True)

    while True:
        print("Attempting socket connection...", flush=True)
        try:
            sio.connect('https://groic.in', transports=['websocket'])
            sio.wait()
        except Exception as e:
            print(f"Socket connection error: {e}", flush=True)
        
        time.sleep(30)

if __name__ == "__main__":
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()

    start_bot_socket()
