"""Dash app callbacks (interactive functionality)"""
import plotly.express as px
from dash import Dash, Input, Output

from data import load_data


def register_callbacks(app: Dash):
    """Register all callbacks"""
    @app.callback(
        Output(component_id='my-first-graph-final', component_property='figure'),
        Input(component_id='radio-buttons-final', component_property='value')
    )
    def update_graph(col_chosen):
        df = load_data()
        fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
        return fig