"""UI components"""
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

from data import load_data


def create_layout():
    """Create app layout"""
    df = load_data()
    
    return dbc.Container([
        dbc.Row([
            html.Div('My First App with Data, Graph, and Controls', 
                    className="text-primary text-center fs-3")
        ]),
        dbc.Row([
            dbc.RadioItems(
                options=[{"label": x, "value": x} for x in ["pop", 'lifeExp', 'gdpPercap']],
                value="lifeExp", inline=True, id='radio-buttons-final')
        ]),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(data=df.to_dict('records'),  # type: ignore
                                    page_size=12, 
                                    style_table={'overflowX': 'auto'})
            ], width=6),
            dbc.Col([
                dcc.Graph(figure={}, id='my-first-graph-final')
            ], width=6),
        ]),
    ], fluid=True)