import requests
from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

API_KEY = '935c6639eb1849e9b6278ee75e954767'
BASE_URL = 'https://api.football-data.org/v2/'

# League IDs (Football Data API IDs for each competition)
LEAGUE_IDS = {
    'Champions League': 2001,
    'Premier League': 2021,
    'La Liga': 2014,
    'Serie A': 2019,
    'Bundesliga': 2002,
    'Ligue 1': 2015
}

def get_matches_by_league(league_id, time_frame):
    # Calculate the dates based on the time frame selected
    now = datetime.utcnow()
    if time_frame == "12 hours":
        end_date = now + timedelta(hours=12)
    elif time_frame == "2 days":
        end_date = now + timedelta(days=2)
    elif time_frame == "5 days":
        end_date = now + timedelta(days=5)
    elif time_frame == "7 days": 
        end_date = now + timedelta(days=7)
    elif time_frame == "14 days":  # Added for 14 days
        end_date = now + timedelta(days=14)

    start_date = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_date = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    print(f"Fetching matches from {start_date} to {end_date}")

    # Set the API endpoint and headers
    url = f"{BASE_URL}matches?competitions={league_id}&dateFrom={start_date}&dateTo={end_date}"
    headers = {
        'X-Auth-Token': API_KEY
    }

    response = requests.get(url, headers=headers)
    
    # Check if the response was successful
    if response.status_code == 200:
        data = response.json()
        return data['matches']  # Return the list of matches
    else:
        print(f"Error fetching data: {response.status_code}, {response.text}")
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    matches_by_league = {}
    if request.method == "POST":
        time_frame = request.form["time_frame"]
        
        # Fetch matches for each league
        for league, league_id in LEAGUE_IDS.items():
            matches_by_league[league] = get_matches_by_league(league_id, time_frame)

    return render_template("index.html", matches=matches_by_league)

if __name__ == "__main__":
    app.run(debug=True)
