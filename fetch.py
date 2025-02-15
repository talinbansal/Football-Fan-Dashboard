from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import requests 
from datetime import datetime
import time
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
YT_API_KEY = os.getenv("YT_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

###########################################################################################################################################################################################################################
################################################################################--Youtube API to Fetch Highlights--##################################################################################################################

@app.route('/api/city_highlights')
def get_city_highlights():
    query='Manchester City Highlights'
    max_results = 6
    
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YT_API_KEY}&maxResults={max_results}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        highlights = data.get('items', [])
        videos = []
        
        for item in highlights:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            thumbnail = item['snippet']['thumbnails']['high']['url']
            video_url = f"https://www.youtube.com/embed/{video_id}" 
            
            videos.append({"title": title, "thumbnail": thumbnail, "video_url": video_url})

        return jsonify(videos)
    else:
        return jsonify({"error": "Failed to fetch videos"}), 500

###########################################################################################################################################################################################################################
################################################################################--Squad Details--##################################################################################################################

## global_p_id = []

@app.route('/api/squad')
def city_squad(): 
    ## global API_KEY
    url = "http://api.football-data.org/v4/teams/65"
    headers = {
        "X-Auth-Token": API_KEY 
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        squad = data.get('squad', {})
        
        ## p_id = []
        players = []
        for p_data in squad:
            player_name = p_data.get('name', '')
            player_pos = p_data.get('position', '')
            player_nation = p_data.get('nationality', '')
            ## player_id = p_data.get('id', '')
            
            create_player = [player_name,  player_pos, player_nation]
            
            players.append(create_player)
            ## p_id.append(player_id)
            
        ## global_p_id = p_id
        
        return jsonify({
            'team_squad': players,
        })
        
    else:
        return jsonify({"error": f"Error: {response.status_code}"}), response.status_code
                    
###########################################################################################################################################################################################################################
################################################################################--Premier League Data--####################################################################################################################

@app.route('/api/team_data')
def get_team_data():
    
    url = "https://api.football-data.org/v4/competitions/PL/standings"
    headers = {"X-Auth-Token": API_KEY}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # The API returns one or more standings sections (e.g., overall table, home/away table)
        standings_sections = data.get("standings", [])
        man_city_found = False

        # Iterate through each standings section
        for section in standings_sections:
            table = section.get("table", [])
            # Iterate through each team's entry in the table
            for team_entry in table:
                team = team_entry.get("team", {})
                if team.get("name") == "Manchester City FC":
                    team_data = {
                        "team_name": "Manchester City FC",
                        "position": team_entry.get("position"),
                        "points": team_entry.get("points"),
                        "played_games": team_entry.get("playedGames"),
                        "won": team_entry.get("won"),
                        "draw": team_entry.get("draw"),
                        "lost": team_entry.get("lost"),
                        "goals_for": team_entry.get("goalsFor"),
                        "goals_conceded": team_entry.get("goalsAgainst"),
                    }
                    man_city_found = True
                    break  # Exit the inner loop once found
            if man_city_found:
                break  # Exit the outer loop if we've already found Man City
        return jsonify(team_data)
        if not man_city_found:
            print("Manchester City FC was not found in the standings data.")
    else:
        print(f"Error: {response.status_code} - {response.text}")


@app.route('/api/pl_team_top_scorer')    
def top_scorer():
    
    url = 'https://api.football-data.org/v4/competitions/PL/scorers'
    headers = {'X-Auth-Token': API_KEY}

    response = requests.get(url, headers=headers)
    
    player_score = {}

    if response.status_code == 200:
        data = response.json()
        
        scorers = data.get("scorers", [])
        
        for player in scorers:
            player_name = player.get('player', {})
            player_goals = player.get('goals', '')
            pen_goals = player.get('penalties', '')
            if pen_goals is None:
                pen_goals = 0
            
            non_pen_goals = int(player_goals) - pen_goals
            
            player_team = player.get('team', {})
            my_team = player_team.get('name', '')
            
            if my_team == 'Manchester City FC':
                player_info = player_name.get('name', '')
                player_score[player_info] = [player_goals, pen_goals, non_pen_goals]
                
        return jsonify({
            'player_score': player_score, 
            })
        
    return jsonify({'error': 'Failed to fetch data'}), response.status_code


@app.route('/api/pl_matches') 
def pl_up_matches():
    
    url = 'https://api.football-data.org/v4/teams/65/matches?status=SCHEDULED'
    headers = {'X-Auth-Token': API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        upcoming_matches = []
        updates_match_details = [] 
        matches = data.get('matches', [])
        
        premier_league_matches = [
            match for match in matches if match.get('competition', {}).get('name') == "Premier League"
        ]
        
        if premier_league_matches:
            for match in premier_league_matches:
                ##match_id = match.get('id')
                ##match_ids.append(match_id)
                
                home_team = match.get('homeTeam',{}).get('tla', 'Unknown')
                away_team = match.get('awayTeam', {}).get('tla', 'Unknown')
                match_date_raw = match.get('utcDate', '')
                
                match_date = datetime.strptime(match_date_raw, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = match_date.strftime("%d/%m/%Y %H:%M")
                formatted_time = match_date.strftime("%H:%M")
                
                match = f"{home_team} vs {away_team} on {formatted_date}"
                updates_match = f"{home_team} {formatted_time} {away_team}" 
                upcoming_matches.append(match)
                updates_match_details.append(updates_match)
                
            return jsonify({
                'upcoming_matches': upcoming_matches,
                'updates_match': updates_match_details,
            })
            
        else:
            print("No upcoming Premier League matches found.")

    else:
        print(f"Error: {response.status_code}, {response.text}")
        
@app.route('/api/pl_live_matches')
def pl_live_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {
        "X-Auth-Token": API_KEY  
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        pl_matches = [match for match in data['matches'] if match['competition']['code'] == "PL"]
        
        live_pl_matches = [match for match in pl_matches if match['status'] in ("LIVE", "IN_PLAY")]
        
        live_man_city_matches = [match for match in live_pl_matches
                                if (match['homeTeam']['name'] == "Manchester City FC" or 
                                    match['awayTeam']['name'] == "Manchester City FC")]
        
        if not live_man_city_matches:
                    result = {
                        "live_match": "No Matches Today",
                        "live_match_score": ""
                    }
        else:
            # If more than one match exists, you can customize this logic
            match = live_man_city_matches[0]
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            score = match['score']['fullTime']
            result = {
                "live_match": f"{home_team} vs {away_team}",
                "live_match_score": f"Score: {score['home']}:{score['away']}"
            }
        return jsonify(result)

    else:
        return jsonify({"error": f"Error: {response.status_code}"}), response.status_code


###########################################################################################################################################################################################################################
################################################################################--Champions League Data--##################################################################################################################

@app.route('/api/team_data_ucl')
def get_team_data_ucl():
    
    url = "https://api.football-data.org/v4/competitions/CL/standings"
    headers = {"X-Auth-Token": API_KEY}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        standings_sections = data.get("standings", [])
        man_city_found = False

        # Iterate through each standings section
        for section in standings_sections:
            table = section.get("table", [])
            # Iterate through each team's entry in the table
            for team_entry in table:
                team = team_entry.get("team", {})
                if team.get("name") == "Manchester City FC":
                    print("yes")
                    team_data = {
                        "team_name": "Manchester City FC",
                        "position": team_entry.get("position"),
                        "points": team_entry.get("points"),
                        "played_games": team_entry.get("playedGames"),
                        "won": team_entry.get("won"),
                        "draw": team_entry.get("draw"),
                        "lost": team_entry.get("lost"),
                        "goals_for": team_entry.get("goalsFor"),
                        "goals_conceded": team_entry.get("goalsAgainst"),
                    }
                    man_city_found = True
                    break  # Exit the inner loop once found
            if man_city_found:
                break  # Exit the outer loop if we've already found Man City
        return jsonify(team_data)
        if not man_city_found:
            print("Manchester City FC was not found in the standings data.")
    else:
        print(f"Error: {response.status_code} - {response.text}")
 
            
@app.route('/api/ucl_team_top_scorer')    
def ucl_top_scorer():
    
    url = 'https://api.football-data.org/v4/competitions/CL/scorers'
    headers = {'X-Auth-Token': API_KEY}

    response = requests.get(url, headers=headers)
    
    player_score = {}

    if response.status_code == 200:
        data = response.json()
        
        scorers = data.get("scorers", [])
        
        for player in scorers:
            player_name = player.get('player', {})
            player_goals = player.get('goals', '')
            pen_goals = player.get('penalties', '')
            if pen_goals is None:
                pen_goals = 0
            
            non_pen_goals = int(player_goals) - pen_goals
            
            player_team = player.get('team', {})
            my_team = player_team.get('name', '')
            
            if my_team == 'Manchester City FC':
                player_info = player_name.get('name', '')
                player_score[player_info] = [player_goals, pen_goals, non_pen_goals]
                
        return jsonify({
            'player_score': player_score, 
            })
        
    return jsonify({'error': 'Failed to fetch data'}), response.status_code

        
@app.route('/api/ucl_matches') 
def ucl_up_matches():
    
    url = 'https://api.football-data.org/v4/teams/65/matches?status=SCHEDULED'
    headers = {'X-Auth-Token': API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        upcoming_matches = []
        match_ids = [] 
        matches = data.get('matches', [])
        
        premier_league_matches = [
            match for match in matches if match.get('competition', {}).get('name') == "UEFA Champions League"
        ]
        
        if premier_league_matches:
            for match in premier_league_matches:
                home_team = match.get('homeTeam',{}).get('tla', 'Unknown')
                away_team = match.get('awayTeam', {}).get('tla', 'Unknown')
                match_date_raw = match.get('utcDate', '')
                
                match_date = datetime.strptime(match_date_raw, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = match_date.strftime("%d/%m/%Y %H:%M")
                
                match = f"{home_team} vs {away_team} on {formatted_date}"
                upcoming_matches.append(match)
            return jsonify({
                'upcoming_matches': upcoming_matches,
            })
            
        else:
            print("No upcoming Champions League matches found.")

    else:
        print(f"Error: {response.status_code}, {response.text}")
        
@app.route('/api/ucl_live_matches')
def ucl_live_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {
        "X-Auth-Token": API_KEY  
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        pl_matches = [match for match in data['matches'] if match['competition']['code'] == "CL"]
        
        live_pl_matches = [match for match in pl_matches if match['status'] in ("LIVE", "IN_PLAY")]
        
        live_man_city_matches = [match for match in live_pl_matches
                                if (match['homeTeam']['name'] == "Manchester City FC" or 
                                    match['awayTeam']['name'] == "Manchester City FC")]
        
        if not live_man_city_matches:
                    result = {
                        "live_match": "No Matches Today",
                        "live_match_score": ""
                    }
        else:
            # If more than one match exists, you can customize this logic
            match = live_man_city_matches[0]
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            score = match['score']['fullTime']
            result = {
                "live_match": f"{home_team} vs {away_team}",
                "live_match_score": f"Score: {score['home']}:{score['away']}"
            }
        return jsonify(result)

    else:
        return jsonify({"error": f"Error: {response.status_code}"}), response.status_code

    

 
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5001)

     
