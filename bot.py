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

# கன்சோலில் இருந்து பெறப்பட்ட முழுமையான நேரடி ID Token
ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImI1MTImMTNpZHRwZCI2ImVpZiZpcCIsImFsZyI6IlJTMjU2In0.eyJhdWQiOiJmcmlyZktleSIsInVzZXJfaWQiOiJFeHBvcnRlZFRva2VuTGF3MzZhMzM0YzYi"
ROOM_ID = "37uqc814uu"

def start_bot_socket():
    print("Bot socket initialization started...", flush=True)
    # லாக்ஸில் முழு விவரம் தெரிய லாக்கரை ஆன் செய்துள்ளோம்
    sio = socketio.Client(logger=True, engineio_logger=True)

    @sio.event
    def connect():
        print("Connected to Groic Socket server successfully!", flush=True)
        sio.emit('joinRoom', {'roomId': ROOM_ID})

    @sio.event
    def disconnect():
        print("Disconnected from Groic server.", flush=True)

    while True:
        if ID_TOKEN:
            print("Connecting to socket with proper handshake...", flush=True)
            try:
                # டிரான்ஸ்போர்ட் கட்டுப்பாட்டை நீக்கிவிட்டு, Header மற்றும் Auth இரண்டையும் அனுப்புகிறோம்
                sio.connect(
                    'https://groic.in', 
                    headers={"Authorization": ID_TOKEN},
                    auth={"token": ID_TOKEN}
                )
                sio.wait()
            except Exception as e:
                print(f"Socket connection error: {e}", flush=True)
        else:
            print("ID Token missing...", flush=True)
        
        time.sleep(30)

if __name__ == "__main__":
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()

    start_bot_socket()
