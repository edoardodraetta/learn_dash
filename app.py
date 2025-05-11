"""Dash app entrypoint"""
import dash_bootstrap_components as dbc
from dash import Dash

from callbacks import register_callbacks
from layout import create_layout

# Initialize the app
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Create layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)