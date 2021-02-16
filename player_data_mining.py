import requests
import json
from datetime import datetime, time, timedelta

def time_to_time_delta(time_str):
    t = datetime.strptime(time_str, '%M:%S') if time_str != '' else  datetime.strptime('00:00', '%M:%S')
    h, m, s = t.hour, t.minute, t.second
    return timedelta(hours=h, minutes=m, seconds=s)

    
def extract_data(json_data):
    keys = ['min', 'pts', 'fgm', 'fga', 'fg_pct', 'ftm', 'fta', 'ft_pct',
            'fg3m', 'fg3a', 'fg3_pct', 'ast', 'reb', 'stl', 'blk', 'turnover']
    
    output = {}
    for key in keys:
        output[key] = []
        for record in json_data['data']:
            value = record.get(key, 0)
            output[key].append(value)
            
    # handle special case to convert minutes:
    output['min'] = list(map(time_to_time_delta, output['min']))
    
    return output

# API to pull player stats

base_url = 'https://www.balldontlie.io/api/v1/stats?seasons[]=2020&per_page[]=100&player_ids[]='

# Cavs players IDs

cavs_dict = {9: {'name': 'Jarrett Allen', 'stats':{}},
        666453: {'name': 'Marques Bolden', 'stats':{}},
        #123: {'name': 'Matthew Delladova', 'stats':{}},
        134: {'name': 'Damyean Dotson', 'stats':{}},
        137: {'name': 'Andre Drummond', 'stats':{}},
        666581: {'name': 'Darius Garland', 'stats':{}},
        285: {'name': 'Kevin Love', 'stats':{}},
        295: {'name': 'Thon Maker', 'stats':{}},
        306: {'name': 'Javale McGee', 'stats':{}},
        3547247: {'name': 'Isaac Okoro', 'stats':{}},
        359: {'name': 'Cedi Osman', 'stats':{}},
        383: {'name': 'Taurean Prince', 'stats':{}},
        413: {'name': 'Collin Sexton', 'stats':{}},
        3547279: {'name': 'Lamar Stevens', 'stats':{}},
        666940: {'name': 'Dean Wade', 'stats':{}},
        666971: {'name': 'Dylan Windler', 'stats':{}},
        }

# Pull Cavs stats using the base API and player IDs. Store data in a list.

# Uncomment below to see the status of the API call
#players_status_test = [requests.get(base_url + str(player_id)) for player_id in cavs_dict]
#print(players_status_test[0].status_code)

players = [requests.get(base_url + str(player_id)).json() for player_id in cavs_dict]

player_stats =[extract_data(player) for player in players]

# Fill the stats for each player in the cavs Dictionary

cavs_dict[9]['stats'] = player_stats[0]
cavs_dict[666453]['stats'] = player_stats[1]
#cavs_dict[123]['stats'] = player_stats[2]
cavs_dict[134]['stats'] = player_stats[2]
cavs_dict[137]['stats'] = player_stats[3]
cavs_dict[666581]['stats'] = player_stats[4]
cavs_dict[285]['stats'] = player_stats[5]
cavs_dict[295]['stats'] = player_stats[6]
cavs_dict[306]['stats'] = player_stats[7]
cavs_dict[3547247]['stats'] = player_stats[8]
cavs_dict[359]['stats'] = player_stats[9]
cavs_dict[383]['stats'] = player_stats[10]
cavs_dict[413]['stats'] = player_stats[11]
cavs_dict[3547279]['stats'] = player_stats[12]
cavs_dict[666940]['stats'] = player_stats[13]
cavs_dict[666971]['stats'] = player_stats[14]
