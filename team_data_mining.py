import requests
import json
from datetime import datetime, date, timedelta

def time_to_time_delta(time_str):
    t = datetime.strptime(time_str[0:10], '%Y-%m-%d')
    game_date = date(t.year, t.month, t.day)
    return game_date

def extract_data(json_data):
    
    keys = ['id', 'date', 'home_team', 'home_team_score', 'period', 'postseason', 
            'status', 'visitor_team', 'visitor_team_score']
    
    output = {}
    
    for key in keys:
        output[key] = []
        for record in json_data['data']:
            value = record.get(key, 0)
            output[key].append(value)
    
    # handle special case to convert minutes:
    output['date'] = list(map(time_to_time_delta, output['date']))

    return output

# API to pull game stats

team_data_url = 'https://www.balldontlie.io/api/v1/games?seasons[]=2020&team_ids[]=6&per_page=100'

# Uncomment below to see the status of the API call
#status_test = requests.get(team_data_url)
#print(status_test.status_code)

# Extract cavs team data

cavs_json_data = requests.get(team_data_url).json()

# Place cavs team data into a dictionary so it can be easily manipulated

cavs_team_data = extract_data(cavs_json_data)

# Function to remove irrelevant data from the 'home' and 'visitor' teams. 
# Function should return the full team name from 'home' and 'visitor' teams and replace the old lists.

def clean_team_names(cavs_dict):
    
    new_home_team = []
    new_away_team = []
    
    for record in cavs_dict['home_team']:
        new_home_team.append(record['full_name'])
    
    for record in cavs_dict['visitor_team']:
        new_away_team.append(record['full_name'])
        
    cavs_dict['home_team'] = new_home_team
    cavs_dict['visitor_team'] = new_away_team

clean_team_names(cavs_team_data)
