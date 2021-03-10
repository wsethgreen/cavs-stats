from flask import Flask, render_template, redirect, url_for, request
from player_data_calcs import cavs_stats
from cavs_data_calcs import results_df, cavs_ppg, opp_ppg, cavs_record

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
    
    return render_template('players.html', cavs_key=key, cavs_stats=cavs_stats,
                        html_nums_df_10=html_nums_df_10, html_pcts_df_10=html_pcts_df_10, 
                        )


# Create the route to host the line graph of the selected players numbers graph
@app.route('/players/<key>/numsgraph', methods = ["POST", "GET"])
def numsgraph(key):
    return render_template(f'/graphs/{key}_nums_graph.html')

# Create the route to host the line graph of the selected players perctents graph
@app.route('/players/<key>/pctsgraph', methods = ["POST", "GET"])
def pctsgraph(key):
    return render_template(f'/graphs/{key}_pcts_graph.html')

# Create the route to host the line graph of the Cavs team results
@app.route('/cavsmap', methods=["GET", "POST"])
def brewmap():
    return render_template('/graphs/cavs_results_map.html')

if __name__ == '__main__':
    app.run()