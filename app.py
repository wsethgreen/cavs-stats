from flask import Flask, render_template, redirect, url_for, request
from player_data_calcs import cavs_stats
from cavs_data_calcs import results_df, cavs_ppg, opp_ppg, cavs_record

app = Flask(__name__)

@app.route('/', methods = ["POST", "GET"])
def index():
    
    html_results_df = results_df.to_html(classes='results_df__table', header="true", index=False)
    
    return render_template('index.html', cavs_stats=cavs_stats, html_results_df=html_results_df,
                           cavs_record=cavs_record, cavs_ppg=cavs_ppg, opp_ppg=opp_ppg)

@app.route('/players/<key>', methods = ["POST", "GET"])
def table(key):
    
    #Create DFs for number and percent stats for the past 10 games for the selected player. 
    reverse_nums_df_10 = cavs_stats[key]['nums_df'].iloc[::-1]
    nums_df_10 = reverse_nums_df_10.head(10)
    html_nums_df_10 = nums_df_10.to_html(classes='df__table', header="true", index=False)
    
    reverse_pcts_df_10 = cavs_stats[key]['pcts_df'].iloc[::-1]
    pcts_df_10 = reverse_pcts_df_10.head(10)
    html_pcts_df_10 = pcts_df_10.to_html(classes='df__table', header="true", index=False)
    
    #Create DFs for number and percent stats for the past 5 games for the selected player. 
    reverse_nums_df_5 = cavs_stats[key]['nums_df'].iloc[::-1]
    nums_df_last_5 = reverse_nums_df_5.head(5)
    html_nums_df_5 = nums_df_last_5.to_html(classes='df__table', header="true", index=False)
    
    reverse_pcts_df_5 = cavs_stats[key]['pcts_df'].iloc[::-1]
    pcts_df_last_5 = reverse_pcts_df_5.head(5)
    html_pcts_df_5 = pcts_df_last_5.to_html(classes='df__table', header="true", index=False)
    
    return render_template('players.html', cavs_key=key, cavs_stats=cavs_stats,
                           html_nums_df_10=html_nums_df_10, html_pcts_df_10=html_pcts_df_10, 
                           html_nums_df_5=html_nums_df_5, html_pcts_df_5=html_pcts_df_5)

if __name__ == '__main__':
    app.run()