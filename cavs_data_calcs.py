from team_data_mining import cavs_team_data
import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta

# Put data in a dataframe to easily manipulate

game_df = pd.DataFrame.from_dict(cavs_team_data)

# Drop rows where teams scored 0 points

game_df.drop(game_df[game_df['home_team_score'] == 0].index, inplace=True)

# Sort the dataframe so the most recent game results appear at the top

game_df.sort_values('date', ascending=False, inplace=True)

# Create a 'result' column to track the cavs record

game_df['result'] = np.where(((game_df['home_team'] == 'Cleveland Cavaliers') & (game_df['home_team_score'] > game_df['visitor_team_score'])) | 
                             ((game_df['visitor_team'] == 'Cleveland Cavaliers') & (game_df['home_team_score'] < game_df['visitor_team_score'])), 
                             'W', 'L')

# Create columns for 'cavs_points' and 'opp_points' to calculate points per game and points given up per game

game_df['cavs_points'] = np.where(game_df['home_team'] == 'Cleveland Cavaliers', 
                                  game_df['home_team_score'], game_df['visitor_team_score'])

game_df['opp_points'] = np.where(game_df['home_team'] != 'Cleveland Cavaliers', 
                                  game_df['home_team_score'], game_df['visitor_team_score']) 

#Create variables to store Cavs and Opponents' average points per game

cavs_ppg = round(game_df['cavs_points'].mean(), 1)
opp_ppg = round(game_df['opp_points'].mean(), 1)

# Create a column of Cavs and Opponents for display purposes

game_df['cavs'] = 'Cleveland Cavaliers'

game_df['opponent'] = np.where(game_df['home_team'] != 'Cleveland Cavaliers', 
                                  game_df['home_team'], game_df['visitor_team'])

# Create a column that displays the cavs as either Home or Away. 
# Leaving column header blank for display purposes

game_df[' '] = np.where(game_df['home_team'] == 'Cleveland Cavaliers', 
                                  'vs.', '@')

# Create a new dataframe to display on the home page of the app 
# i.e. strip away unnecessary columns

results_df = game_df[['date', 'cavs', 'cavs_points', ' ', 'opp_points','opponent', 'result']].copy()

results_df.rename(columns={'date': 'Date', 'cavs': 'Cavs', 'cavs_points': 'Score', ' ': ' ',
                           'opp_points': 'Score', 'opponent': 'Opponent', 'result': 'Result'}, inplace=True)

# Create dictionary to track the Cavs record

cavs_record = results_df['Result'].value_counts().to_dict()
