
from flask import Flask, request, render_template_string, send_from_directory
import requests
import firebase_admin
from firebase_admin import credentials, messaging
import time
import os
import json

app = Flask(__name__)

# Load Firebase credentials securely from environment variable
cred_json = json.loads(os.environ['FIREBASE_JSON'])
cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

# List of FCM device tokens (replace with real tokens)
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
                team_id = play.get('team', {}).get('id', '')
                timestamp = play.get('about', {}).get('startTime', '')
                hr_events.append({
                    "text": f"{batter} hit a HR for {team}!",
                    "time": timestamp,
                    "team_id": team_id
                })

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
    return """
    <html>
    <head><title>MLB Home Run Alerts</title></head>
    <body style='background-color:#461D7C; color:#FDD023; font-family:sans-serif; text-align:center;'>
    <img src='/static/logo.png' alt='Logo' style='margin-top:30px; height:80px;'>
    <h1>Welcome to MLB Home Run Alerts</h1>
    <p>Click below to view today's home run alerts in real time.</p>
    <a href='/check-hr' style='display:inline-block;padding:12px 24px;background:#FDD023;color:#461D7C;font-weight:bold;border-radius:8px;text-decoration:none;'>Check Home Runs</a>
    </body>
    </html>
    """

@app.route("/check-hr")
def check_home_runs():
    events = get_home_run_events()
    if not events:
        return render_template_string("""
        <html>
        <head><title>HR Alerts</title></head>
        <body style='background-color:#461D7C; color:#FDD023; font-family:sans-serif; text-align:center;'>
        <img src='/static/logo.png' alt='Logo' style='margin-top:20px; height:60px;'>
        <h1>No Home Runs Yet</h1>
        <a href='/check-hr' style='display:inline-block;padding:10px 20px;background:#FDD023;color:#461D7C;font-weight:bold;border-radius:6px;text-decoration:none;'>Refresh</a>
        </body>
        </html>
        """)

    event_html = ''.join(
        f"<li style='margin-bottom:15px;'><img src='https://www.mlbstatic.com/team-logos/{hr['team_id']}.svg' alt='team logo' style='height:25px;vertical-align:middle;margin-right:10px;'> {hr['text']} <br><small>{hr['time']}</small></li>"
        for hr in events
    )

    return f"""
    <html>
    <head><title>HR Alerts</title></head>
    <body style='background-color:#461D7C; color:#FDD023; font-family:sans-serif;'>
    <div style='text-align:center;'>
    <img src='/static/logo.png' alt='Logo' style='margin-top:20px; height:60px;'>
    <h1>Home Run Alerts</h1>
    <a href='/check-hr' style='display:inline-block;padding:10px 20px;margin-bottom:20px;background:#FDD023;color:#461D7C;font-weight:bold;border-radius:6px;text-decoration:none;'>Refresh</a>
    </div>
    <ul>{event_html}</ul>
    </body>
    </html>
    """

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
