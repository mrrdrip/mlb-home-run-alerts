
from flask import Flask, render_template_string
import os

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>Mr. Drip's Home Run Alerts</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background-color: #461D7C;
      color: #FDD023;
      text-align: center;
    }
    header {
      padding: 2rem 1rem 0;
    }
    header img {
      max-height: 120px;
    }
    h1 {
      margin: 0.5rem 0 0.2rem;
      font-size: 2.2rem;
    }
    p {
      margin-top: 0;
      font-size: 1rem;
      opacity: 0.9;
    }
    .check-section {
      margin: 2rem auto;
    }
    button {
      padding: 0.8rem 1.5rem;
      font-weight: bold;
      border: none;
      border-radius: 8px;
      background-color: #FDD023;
      color: #461D7C;
      font-size: 1.1rem;
      cursor: pointer;
    }
    table {
      width: 90%;
      margin: 2rem auto;
      border-collapse: collapse;
      background: #fff;
      color: #000;
      border-radius: 12px;
      overflow: hidden;
    }
    thead {
      background-color: #FDD023;
      color: #461D7C;
    }
    th, td {
      padding: 0.8rem;
      text-align: center;
      border-bottom: 1px solid #ccc;
    }
    th:first-child, td:first-child {
      text-align: left;
    }
    .section-title {
      font-size: 1.6rem;
      margin-top: 3rem;
      margin-bottom: 1rem;
      border-bottom: 2px solid #FDD023;
      display: inline-block;
      padding-bottom: 0.4rem;
    }
  </style>
</head>
<body>
  <header>
    <img src='https://mlb-home-run-alerts.onrender.com/static/logo.png' alt='Mr. Drip Logo' />
    <h1>Mr. Drip's Home Run Alerts</h1>
    <p>Powered by live MLB stats & matchup analytics</p>
  </header>

  <div class='check-section'>
    <button onclick='alert("Live home run check feature coming soon!")'>💣 Check for Home Runs</button>
    <div id='hr-results' style='margin-top: 1rem;'></div>
  </div>

  <div class='section-title'>Drip's Daily Power Hitters</div>
  <table>
    <thead>
      <tr>
        <th>Player</th>
        <th>Team</th>
        <th>AVG</th>
        <th>HR</th>
        <th>OBP</th>
        <th>SLG</th>
        <th>Pitcher</th>
        <th>Matchup Score</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Aaron Judge</td>
        <td>NYY</td>
        <td>.298</td>
        <td>12</td>
        <td>.420</td>
        <td>.622</td>
        <td>Chris Sale (L)</td>
        <td>87</td>
      </tr>
      <tr>
        <td>Juan Soto</td>
        <td>NYY</td>
        <td>.312</td>
        <td>10</td>
        <td>.446</td>
        <td>.594</td>
        <td>Tanner Houck (R)</td>
        <td>85</td>
      </tr>
      <tr>
        <td>Yordan Alvarez</td>
        <td>HOU</td>
        <td>.288</td>
        <td>9</td>
        <td>.397</td>
        <td>.580</td>
        <td>Kenta Maeda (R)</td>
        <td>83</td>
      </tr>
    </tbody>
  </table>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)
