from flask import Flask, render_template, redirect, url_for, request
from player_data_calcs import cavs_stats
from cavs_data_calcs import results_df, cavs_ppg, opp_ppg, cavs_record
import plotly.graph_objects as go
import plotly.io as pio

# Create App
app = Flask(__name__)

# Create the route of the home page for the app
@app.route('/', methods = ["POST", "GET"])
def index():
    # Create a variable which transforms the Cavs' team results 
    # from a dataframe to html
    html_results_df = results_df.to_html(classes='results_df__table', header="true", index=False)
    
    return render_template('index.html', cavs_stats=cavs_stats, html_results_df=html_results_df,
                           cavs_record=cavs_record, cavs_ppg=cavs_ppg, opp_ppg=opp_ppg)

# Create the route of the 'players' page for the app
@app.route('/players/<key>', methods = ["POST", "GET"])
def players(key):
    
    #Create DFs for number and percent stats for the past 10 games for the selected player.
    # Create the players "numbers" df 
    nums_df_10 = cavs_stats[key]['nums_df'].head(10)
    nums_df_10.sort_values('DATE', ascending=False, inplace=True)
    html_nums_df_10 = nums_df_10.to_html(classes='df__table', header="true", index=False)
    # Create the players "percents" df 
    pcts_df_10 = cavs_stats[key]['pcts_df'].head(10)
    pcts_df_10.sort_values('DATE', ascending=False, inplace=True)
    html_pcts_df_10 = pcts_df_10.to_html(classes='df__table', header="true", index=False)
    
    #Create DFs for number and percent stats for the past 5 games for the selected player.
    # Create the players "numbers" df  
    nums_df_5 = cavs_stats[key]['nums_df'].head(5)
    nums_df_5.sort_values('DATE', ascending=False, inplace=True)
    html_nums_df_5 = nums_df_5.to_html(classes='df__table', header="true", index=False)
    # Create the players "percents" df 
    pcts_df_5 = cavs_stats[key]['pcts_df'].head(5)
    pcts_df_5.sort_values('DATE', ascending=False, inplace=True)
    html_pcts_df_5 = pcts_df_5.to_html(classes='df__table', header="true", index=False)
    
    # Create the player numbers graph
    # create figure
    num_graph = go.Figure()
    
    # Add points, rebounds, and assist lines
    num_graph.add_trace(go.Scatter(x=cavs_stats[key]['nums_df']['DATE'], y=cavs_stats[key]['nums_df']['PTS'],
                    mode='lines+markers', name='Points', 
                    line=dict(color='rgb(134,0,56)', width=2)))

    num_graph.add_trace(go.Scatter(x=cavs_stats[key]['nums_df']['DATE'], y=cavs_stats[key]['nums_df']['REB'],
                    mode='lines+markers', name='Rebounds', 
                    line=dict(color='rgb(4,30,66)', width=2)))

    num_graph.add_trace(go.Scatter(x=cavs_stats[key]['nums_df']['DATE'], y=cavs_stats[key]['nums_df']['AST'],
                    mode='lines+markers', name='Assists', 
                    line=dict(color='rgb(253,187,48)', width=2)))
    
    num_graph.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, title=f'{key} Season Results',
                    xaxis_title='Date', yaxis_title='Points, Rebounds, Assists')
    
    pio.write_html(num_graph, file='templates/graphs/players_nums_graph.html', auto_open=False)
    
    # Create the player percents graph
    # create figure
    pct_graph = go.Figure()
    
    # Add fg%, ft%, and fg3% points
    pct_graph.add_trace(go.Scatter(x=cavs_stats[key]['pcts_df']['DATE'], y=cavs_stats[key]['pcts_df']['FG%'],
                    mode='markers', name='FG%', 
                    line=dict(color='rgb(134,0,56)', width=2)))

    pct_graph.add_trace(go.Scatter(x=cavs_stats[key]['pcts_df']['DATE'], y=cavs_stats[key]['pcts_df']['FT%'],
                    mode='markers', name='FT%', 
                    line=dict(color='rgb(4,30,66)', width=2)))

    pct_graph.add_trace(go.Scatter(x=cavs_stats[key]['pcts_df']['DATE'], y=cavs_stats[key]['pcts_df']['FG3%'],
                    mode='markers', name='FG3%', 
                    line=dict(color='rgb(253,187,48)', width=2)))
    
    pct_graph.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, title=f'{key} Season Results',
                    xaxis_title='Date', yaxis_title='FG%, FT%, FG3%')
    
    pio.write_html(pct_graph, file='templates/graphs/players_pcts_graph.html', auto_open=False)
    
    return render_template('players.html', cavs_key=key, cavs_stats=cavs_stats,
                           html_nums_df_10=html_nums_df_10, html_pcts_df_10=html_pcts_df_10, 
                           html_nums_df_5=html_nums_df_5, html_pcts_df_5=html_pcts_df_5)

# Create the route to host the line graph of the selected players numbers graph
@app.route('/players/<key>/numsgraph', methods = ["POST", "GET"])
def numsgraph(key):
    return render_template('/graphs/players_nums_graph.html')

# Create the route to host the line graph of the selected players perctents graph
@app.route('/players/<key>/pctsgraph', methods = ["POST", "GET"])
def pctsgraph(key):
    return render_template('/graphs/players_pcts_graph.html')

# Create the route to host the line graph of the Cavs team results
@app.route('/cavsmap', methods=["GET", "POST"])
def brewmap():
    return render_template('/graphs/cavs_results_map.html')

if __name__ == '__main__':
    app.run()