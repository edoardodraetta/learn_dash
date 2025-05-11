"""A dash app with data"""
import pandas as pd
from dash import Dash, dash_table, html

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app (the dash constructor)
app = Dash()

# App components to display
app.layout = [
    html.Div(children='My First App with Data'),
    dash_table.DataTable(
        data=df.to_dict('records'), page_size=10 # type: ignore
    )
    ]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)