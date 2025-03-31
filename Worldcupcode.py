# Published Dashboard URL: https://your-dashboard-url.render.com  
# Password: your_password_if_applicable

import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load and preprocess the data
data = pd.read_csv("worldcupdata.csv")

# Ensure West Germany and Germany are treated as the same country
data['Winner'] = data['Winner'].replace({'West Germany': 'Germany'})
data['Runner-up'] = data['Runner-up'].replace({'West Germany': 'Germany'})

# Create a summary dataset of World Cup wins by country
winners_count = data['Winner'].value_counts().reset_index()
winners_count.columns = ['Country', 'Wins']

# Create the choropleth map figure using Plotly Express
choropleth_fig = px.choropleth(
    winners_count,
    locations='Country',
    locationmode="country names",
    color='Wins',
    color_continuous_scale='Viridis',
    title="FIFA World Cup Wins by Country"
)

# List of all winning countries for display
all_winners = sorted(data['Winner'].unique())

# List of years in the dataset
years = sorted(data['Year'].unique())

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "World Cup Dashboard"
server = app.server

# App layout definition
app.layout = html.Div([
    html.H1("FIFA World Cup Winners & Runner-ups Dashboard"),
    
    # Choropleth Map
    dcc.Graph(
        id='choropleth-map',
        figure=choropleth_fig
    ),
    
    # Display all winning countries
    html.H2("All Countries That Have Ever Won the World Cup:"),
    html.Ul([html.Li(country) for country in all_winners]),
    
    # Dropdown for Country Wins Lookup
    html.H2("Country Wins Lookup"),
    html.Div([
        html.Label("Select a Country:"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in all_winners],
            placeholder="Select a country"
        ),
        html.Div(id='country-wins-output', style={'marginTop': 20})
    ]),
    
    # Dropdown for Yearly Final Lookup
    html.H2("Yearly Final Lookup"),
    html.Div([
        html.Label("Select a Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in years],
            placeholder="Select a year"
        ),
        html.Div(id='year-final-output', style={'marginTop': 20})
    ])
])

# Callback to update the number of wins for a selected country
@app.callback(
    Output('country-wins-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_wins(selected_country):
    if selected_country is None:
        return "Please select a country to see the number of wins."
    wins = (data['Winner'] == selected_country).sum()
    return f"{selected_country} has won the World Cup {wins} time(s)."

# Callback to update the winner and runner-up details for a selected year
@app.callback(
    Output('year-final-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_final(selected_year):
    if selected_year is None:
        return "Please select a year to see the final match details."
    filtered = data[data['Year'] == selected_year]
    if filtered.empty:
        return f"No data available for the year {selected_year}."
    winners = filtered['Winner'].unique()
    runners_up = filtered['Runner-up'].unique()
    winners_str = ", ".join(winners)
    runners_str = ", ".join(runners_up)
    return f"In {selected_year}, Winner(s): {winners_str} | Runner-up(s): {runners_str}"

if __name__ == '__main__':
    app.run_server(debug=True)
