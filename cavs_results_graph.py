import plotly.graph_objects as go
import plotly.io as pio
from player_data_calcs import cavs_stats

# Create team results line graph

fig = go.Figure()

fig.add_trace(go.Scatter(x=game_df['date'], y=game_df['cavs_points'],
                    mode='lines+markers', name='Cavs Points', 
                    line=dict(color='rgb(134,0,56)', width=2)))

fig.add_trace(go.Scatter(x=game_df['date'], y=game_df['opp_points'],
                    mode='lines+markers', name='Opponent Points',
                    line=dict(color='rgb(253,187,48)', width=2)))

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title='Season Results',
                  xaxis_title='Date', yaxis_title='Points Scored')

# fig.show()

pio.write_html(fig, file='templates/graphs/cavs_results_map.html', auto_open=False)