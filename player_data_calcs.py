import pandas as pd
from datetime import datetime, time, timedelta
from player_data_mining import cavs_dict


# Create dataframes out of each players' stats. 
# Create a new key, value pair for the data frame in each players' existing dictionary.

allen_df = pd.DataFrame.from_dict(cavs_dict[9]['stats'])
bolden_df = pd.DataFrame.from_dict(cavs_dict[666453]['stats'])
# delly_df = pd.DataFrame.from_dict(cavs_dict[123]['stats'])
dotson_df = pd.DataFrame.from_dict(cavs_dict[134]['stats'])
drummond_df = pd.DataFrame.from_dict(cavs_dict[137]['stats'])
garland_df = pd.DataFrame.from_dict(cavs_dict[666581]['stats'])
love_df = pd.DataFrame.from_dict(cavs_dict[285]['stats'])
maker_df = pd.DataFrame.from_dict(cavs_dict[295]['stats'])
mcgee_df = pd.DataFrame.from_dict(cavs_dict[306]['stats'])
okoro_df = pd.DataFrame.from_dict(cavs_dict[3547247]['stats'])
osman_df = pd.DataFrame.from_dict(cavs_dict[359]['stats'])
prince_df = pd.DataFrame.from_dict(cavs_dict[383]['stats'])
sexton_df = pd.DataFrame.from_dict(cavs_dict[413]['stats'])
stevens_df = pd.DataFrame.from_dict(cavs_dict[3547279]['stats'])
wade_df = pd.DataFrame.from_dict(cavs_dict[666940]['stats'])
windler_df = pd.DataFrame.from_dict(cavs_dict[666971]['stats'])

# Need to add delly to the cavs_dfs list below when he plays a game

cavs_dfs = [allen_df, bolden_df, dotson_df, drummond_df, garland_df, love_df, maker_df, mcgee_df,
            okoro_df, osman_df, prince_df, sexton_df, stevens_df, wade_df, windler_df]


# Drop rows from dataframes where players recorded 0 minutes, 0 seconds of playing time

no_min = timedelta(hours=0, minutes=0, seconds=0)

for df in cavs_dfs:
    df.drop(df[df['min'] == no_min].index, inplace=True)


# Function to create new dictionary to hold stat calculations for each player

def stats_dict():
    
    player_dict = {}
    
    categories = ['min', 'pts', 'fgm', 'fga', 'fg_pct', 'ftm', 'fta', 'ft_pct', 
            'fg3m', 'fg3a', 'fg3_pct', 'ast', 'reb', 'stl', 'blk', 'turnover']
    
    averages = {}
    past_5_avgs = {}
    highs = {}
    lows = {}
    
    for cat in categories:
        averages[cat] = 0
        past_5_avgs[cat] = 0
        highs[cat] = 0
        lows[cat] = 0


    player_dict['averages'] = averages
    player_dict['past 5'] = past_5_avgs
    player_dict['highs'] = highs
    player_dict['lows'] = lows
    
    return player_dict

allen_dict = stats_dict()
bolden_dict = stats_dict()
# delly_dict = stats_dict()
dotson_dict = stats_dict()
drummond_dict = stats_dict()
garland_dict = stats_dict()
love_dict = stats_dict()
maker_dict = stats_dict()
mcgee_dict = stats_dict()
okoro_dict = stats_dict()
osman_dict = stats_dict()
prince_dict = stats_dict()
sexton_dict = stats_dict()
stevens_dict = stats_dict()
wade_dict = stats_dict()
windler_dict = stats_dict()


# Function to calculate statistics for each player

def stat_calcs(player_dict, player_df):
    
    # Calculate the number of games played for each player
    
    player_dict['games'] = player_df['min'].count()
    
    # The last 5 games played for each player
    tail = player_df.tail(5)
    
    # Calculate average minutes per game
    
    min = 'min'
    
    avg_min = player_df[min].mean(numeric_only=False)
    rounded_avg_min = avg_min.round('1s')
    avg_min_display = str(rounded_avg_min)
    
    # Calculate average minutes played over the past 5 games
    
    avg_5_min = tail[min].mean(numeric_only=False)
    rounded_avg_5_min = avg_5_min.round('1s')
    avg_5_min_display = str(rounded_avg_5_min)
    
    # Calculate season highs/lows for minutes played
    
    high_min = player_df[min].max()
    low_min = player_df[min].min()
    rounded_high_min = high_min.round('1s')
    rounded_low_min = low_min.round('1s')
    high_min_display = str(rounded_high_min)
    low_min_display = str(rounded_low_min)
    
    player_dict['averages'][min] = avg_min_display[-5:]
    player_dict['past 5'][min] = avg_5_min_display[-5:]
    player_dict['highs'][min] = high_min_display[-5:]
    player_dict['lows'][min] = low_min_display[-5:]
    
    # Calculate the season averages, past 5 game averages, season highs, 
    # and season lows for each 'number' category.
    
    # Calculate the season averages for each number category
    
    num_cats = ['pts', 'fgm', 'fga', 'ftm', 'fta', 'fg3m', 
            'fg3a', 'ast', 'reb', 'stl', 'blk', 'turnover']
    
    for cat in num_cats:
        player_dict['averages'][cat] = round(player_df[cat].mean(), 1)
        player_dict['past 5'][cat] = round(tail[cat].mean(), 1)
        player_dict['highs'][cat] = round(player_df[cat].max(), 1)
        player_dict['lows'][cat] = round(player_df[cat].min(), 1)

    # Calculate average shooting percentages per game
    
    fg_made = player_df['fgm'].sum()
    fg_attempt = player_df['fga'].sum()
    ft_made = player_df['ftm'].sum()
    ft_attempt = player_df['fta'].sum()
    fg3_made = player_df['fg3m'].sum()
    fg3_attempt = player_df['fg3a'].sum()
    
    player_dict['averages']['fg_pct'] = 0 if fg_attempt == 0 else round(fg_made/fg_attempt * 100, 1)
    player_dict['averages']['ft_pct'] = 0 if ft_attempt == 0 else round(ft_made/ft_attempt * 100, 1)
    player_dict['averages']['fg3_pct'] = 0 if fg3_attempt == 0 else round(fg3_made/fg3_attempt * 100, 1)
    
    # Calculate the average shooting percentages over the past 5 games
    
    past_5_fg_made = tail['fgm'].sum()
    past_5_fg_attempt = tail['fga'].sum()
    past_5_ft_made = tail['ftm'].sum()
    past_5_ft_attempt = tail['fta'].sum()
    past_5_fg3_made = tail['fg3m'].sum()
    past_5_fg3_attempt = tail['fg3a'].sum()
    
    player_dict['past 5']['fg_pct'] = 0 if past_5_fg_attempt == 0 else round(past_5_fg_made/past_5_fg_attempt * 100, 1)
    player_dict['past 5']['ft_pct'] = 0 if past_5_ft_attempt == 0 else round(past_5_ft_made/past_5_ft_attempt * 100, 1)
    player_dict['past 5']['fg3_pct'] = 0 if past_5_fg3_attempt == 0 else round(past_5_fg3_made/past_5_fg3_attempt * 100, 1)
    
    
    # Calculate the season highs/lows for shooting percentages
    
    pct_cats = ['fg_pct', 'ft_pct', 'fg3_pct']
    
    for cat in pct_cats:
        player_dict['highs'][cat] = player_df[cat].max()
        player_dict['lows'][cat] = player_df[cat].min()


# Fill each players stats dictionary with the appropriate stats

stat_calcs(allen_dict, allen_df)
stat_calcs(bolden_dict, bolden_df)
# stat_calcs(delly_dict, delly_df)
stat_calcs(dotson_dict, dotson_df)
stat_calcs(drummond_dict, drummond_df)
stat_calcs(garland_dict, garland_df)
stat_calcs(love_dict, love_df)
stat_calcs(maker_dict, maker_df)
stat_calcs(mcgee_dict, mcgee_df)
stat_calcs(okoro_dict, okoro_df)
stat_calcs(osman_dict, osman_df)
stat_calcs(prince_dict, prince_df)
stat_calcs(sexton_dict, sexton_df)
stat_calcs(stevens_dict, stevens_df)
stat_calcs(wade_dict, wade_df)
stat_calcs(windler_dict, windler_df)


# Function to make the dataframes easier to digest

def clean_df(df):
    
    # Update the min column to be strings so they are cleaner when displayed
    min_string = []
    for record in df['min']:
        min_string.append(str(record)[-5:])
    
    df['min'] = min_string
    
    # Update the name of each column so it's cleaner when displayed
    
    df = df.rename(columns={'min': 'MIN', 'pts': 'PTS', 'fgm': 'FGM', 'fga': 'FGA',
                            'fg_pct': 'FG%', 'ftm': 'FTM', 'fta': 'FTA', 
                            'ft_pct': 'FT%', 'fg3m': 'FG3M', 'fg3a': 'FG3A',
                            'fg3_pct': 'FG3%', 'ast': 'AST', 'reb': 'REB',
                            'stl': 'STL', 'blk': 'BLK', 'turnover': 'TO'
                            }, inplace=True)

for df in cavs_dfs:
    clean_df(df)

# Create final dictionary to house all relevant data to be displayed 

cavs_stats = {'Jarrett Allen': {'df': allen_df, 'stats': allen_dict},
            'Marques Bolden': {'df': bolden_df, 'stats': bolden_dict},
            #'Matthew Delladova': {'df': delly_df, 'stats': delly_dict},
            'Damyean Dotson': {'df': dotson_df, 'stats': dotson_dict},
            'Andre Drummond': {'df': drummond_df, 'stats': drummond_dict},
            'Darius Garland': {'df': garland_df, 'stats': garland_dict},
            'Kevin Love': {'df': love_df, 'stats': love_dict},
            'Thon Maker': {'df': maker_df, 'stats': maker_dict},
            'Javale McGee': {'df': mcgee_df, 'stats': mcgee_dict},
            'Isaac Okoro': {'df': okoro_df, 'stats': okoro_dict},
            'Cedi Osman': {'df': osman_df, 'stats': osman_dict},
            'Taurean Prince': {'df': prince_df, 'stats': prince_dict},
            'Collin Sexton': {'df': sexton_df, 'stats': sexton_dict},
            'Lamar Stevens': {'df': stevens_df, 'stats': stevens_dict},
            'Dean Wade': {'df': wade_df, 'stats': wade_dict},
            'Dylan Windler': {'df': windler_df, 'stats': windler_dict}
        }
