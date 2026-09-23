import os
import time
import requests

# உங்கள் Firebase மற்றும் Groic ரூம் விவரங்கள்
REFRESH_TOKEN = "உங்கள்_REFRESH_TOKEN"
API_KEY = "உங்கள்_API_KEY"
ROOM_ID = "37uqc814uu"

def send_message(text):
    # இங்கே உங்கள் பாட் அனுப்ப வேண்டிய API கோரிக்கைகளை அமைக்கவும்
    print(f"Sending message to room {ROOM_ID}: {text}")

def main():
    print("Groic bot started successfully as a Background Worker!")
    while True:
        # பாட் தொடர்ந்து இயங்குவதற்கான லூப்
        time.sleep(10)

if __name__ == "__main__":
    main()
