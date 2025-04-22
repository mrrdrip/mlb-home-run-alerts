
from flask import Flask, render_template, request
import requests
import firebase_admin
from firebase_admin import credentials, messaging
import time
import os
import json

app = Flask(__name__)

# Load Firebase credentials from environment variable
cred_json = json.loads(os.environ['FIREBASE_JSON'])
cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

device_tokens = [
    "your-device-token-here"
]

def get_home_run_events():
    date = time.strftime("%Y-%m-%d")
    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date}"
    response = requests.get(schedule_url)
    data = response.json()
    games = data.get("dates", [])[0].get("games", [])
    hr_events = []

    for game in games:
        game_id = game['gamePk']
        feed_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live"
        feed = requests.get(feed_url).json()
        all_plays = feed.get("liveData", {}).get("plays", {}).get("allPlays", [])
        for play in all_plays:
            if play.get("result", {}).get("event") == "Home Run":
                batter = play['matchup']['batter']['fullName']
                team = play.get('team', {}).get('name', 'Unknown')
                hr_events.append(f"{batter} hit a HR for {team}!")

    return hr_events

def send_push_alert(message_body):
    for token in device_tokens:
        message = messaging.Message(
            notification=messaging.Notification(
                title="Home Run Alert!",
                body=message_body
            ),
            token=token
        )
        response = messaging.send(message)
        print(f"Sent message to {token}: {response}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check-hr")
def check_home_runs():
    events = get_home_run_events()
    if not events:
        return "No HRs yet."
    for hr in events:
        send_push_alert(hr)
    return f"Sent alerts for: {', '.join(events)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
