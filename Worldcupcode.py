# URL: https://three21ass7.onrender.com 

import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

data = pd.read_csv("worldcupdata.csv")

data['Winner'] = data['Winner'].replace({
    'West Germany': 'Germany',
    'England': 'United Kingdom'
})
data['Runner-up'] = data['Runner-up'].replace({
    'West Germany': 'Germany',
    'England': 'United Kingdom'
})

winners_count = data['Winner'].value_counts().reset_index()
winners_count.columns = ['Country', 'Wins']

choropleth_fig = px.choropleth(
    winners_count,
    locations='Country',
    locationmode='country names',
    color='Wins',
    hover_name='Country',  # Display country name on hover
    color_continuous_scale='Plasma',  # You can try other scales like 'Viridis', 'Blues', 'Turbo', etc.
    range_color=(0, winners_count['Wins'].max()),
    labels={'Wins': 'Number of World Cup Wins'},
    title='FIFA World Cup Wins by Country'
)

# Update the layout for a cleaner look
choropleth_fig.update_layout(
    template='plotly_white',         # Light background
    margin=dict(l=0, r=0, t=50, b=0), # Tight margins around the figure
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'  # Natural Earth projection looks nicer
    )
)

all_winners = sorted(data['Winner'].unique())
years = sorted(data['Year'].unique())

app = dash.Dash(__name__)
app.title = "World Cup Dashboard"
server = app.server

app.layout = html.Div([
    html.H1("FIFA Soccer World Cup Dashboard"),
    dcc.Graph(
        id='choropleth-map',
        figure=choropleth_fig
    ),
    html.H2("All Countries That Have Ever Won the World Cup:"),
    html.Ul([html.Li(country) for country in all_winners]),
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

@app.callback(
    Output('country-wins-output', 'children'),
    Input('country-dropdown', 'value')
)

def update_country_wins(selected_country):
    if selected_country is None:
        return "Please select a country to see the number of wins."
    wins = (data['Winner'] == selected_country).sum()
    return f"{selected_country} has won the World Cup {wins} time(s)."

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
