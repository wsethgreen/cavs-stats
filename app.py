from flask import Flask, render_template, redirect, url_for, request
from player_data_calcs import cavs_stats
from cavs_data_calcs import results_df, cavs_ppg, opp_ppg, cavs_record

app = Flask(__name__)

@app.route('/', methods = ["POST", "GET"])
def index():
    
    html_results_df = results_df.to_html(classes='results_df__table', header="true", index=False)
    
    return render_template('index.html', cavs_stats=cavs_stats, html_results_df=html_results_df,
                           cavs_record=cavs_record, cavs_ppg=cavs_ppg, opp_ppg=opp_ppg)

@app.route('/table/<key>', methods = ["POST", "GET"])
def table(key):
    
    reverse_df_10 = cavs_stats[key]['df'].iloc[::-1]
    df_10 = reverse_df_10.head(10)
    html_df_10 = df_10.to_html(classes='df__table', header="true", index=False)
    
    reverse_df_5 = cavs_stats[key]['df'].iloc[::-1]
    df_last_5 = reverse_df_5.head(5)
    html_df_5 = df_last_5.to_html(classes='df__table', header="true", index=False)
    
    return render_template('table.html', cavs_key=key, cavs_stats=cavs_stats,
                           html_df_10=html_df_10, html_df_5=html_df_5)

if __name__ == '__main__':
    app.run()