"""A dash app with graphs"""
import pandas as pd
import plotly.express as px
from dash import Dash, dash_table, dcc, html

# dcc = dash core components

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app (the dash constructor)
app = Dash()

# App components to display
app.layout = [
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10), # type: ignore
    dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
    ]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)