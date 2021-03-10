import plotly.graph_objects as go
import plotly.io as pio
from player_data_calcs import cavs_stats

# Create functions that will create a graph for each player to display on the site

def create_graphs(dictionary):
    
    # Create graphs for the "number" categories
    for key in dictionary:
        # create figure
        fig = go.Figure()
        
        # Add points, rebounds, and assist lines
        fig.add_trace(go.Scatter(x=dictionary[key]['nums_df']['DATE'], y=dictionary[key]['nums_df']['PTS'],
                        mode='lines+markers', name='Points', 
                        line=dict(color='rgb(134,0,56)', width=2)))

        fig.add_trace(go.Scatter(x=dictionary[key]['nums_df']['DATE'], y=dictionary[key]['nums_df']['REB'],
                        mode='lines+markers', name='Rebounds', 
                        line=dict(color='rgb(4,30,66)', width=2)))

        fig.add_trace(go.Scatter(x=dictionary[key]['nums_df']['DATE'], y=dictionary[key]['nums_df']['AST'],
                        mode='lines+markers', name='Assists', 
                        line=dict(color='rgb(253,187,48)', width=2)))
        
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, title=f'{key} Season Results',
                        xaxis_title='Date', yaxis_title='Points, Rebounds, Assists')
        
        pio.write_html(fig, file=f'templates/graphs/{key}_nums_graph.html', auto_open=False)
        
        dictionary[key]['nums_graph'] = f'/graphs/{key}_nums_graph.html'
    
    # Create graphs for the "percent" categories
    for key in dictionary:
        # create figure
        fig = go.Figure()
        
        # Add points, rebounds, and assist lines
        fig.add_trace(go.Scatter(x=dictionary[key]['pcts_df']['DATE'], y=dictionary[key]['pcts_df']['FG%'],
                        mode='markers', name='FG %', 
                        line=dict(color='rgb(134,0,56)', width=2)))

        fig.add_trace(go.Scatter(x=dictionary[key]['pcts_df']['DATE'], y=dictionary[key]['pcts_df']['FT%'],
                        mode='markers', name='FT %', 
                        line=dict(color='rgb(4,30,66)', width=2)))

        fig.add_trace(go.Scatter(x=dictionary[key]['pcts_df']['DATE'], y=dictionary[key]['pcts_df']['FG3%'],
                        mode='markers', name='FG3 %', 
                        line=dict(color='rgb(253,187,48)', width=2)))
        
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, title=f'{key} Season Results',
                        xaxis_title='Date', yaxis_title='Points, Rebounds, Assists')
        
        pio.write_html(fig, file=f'templates/graphs/{key}_pcts_graph.html', auto_open=False)
        
        dictionary[key]['pcts_graph'] = f'/graphs/{key}_pcts_graph.html'

# Call function to create all player graphs
create_graphs(cavs_stats)
