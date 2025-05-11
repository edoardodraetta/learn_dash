"""A dash app with controls and callbacks"""
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dash_table, dcc, html

# dcc = dash core components

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app (the dash constructor)
app = Dash()

# App components to display
app.layout = [
    html.Div(className='row', children='My First App with Data, Graph, and Controls',
             style={'textAlign': 'center', 'color':'blue', 'fontSize': 30}),

    html.Div(className='row', children=[
        dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], 
                       value='lifeExp', 
                       inline=True,
                       id='my-radio-buttons-final'),
    ]),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(
                data=df.to_dict('records'), page_size=11,  # type: ignore
                style_table={'overflowX': 'auto'}),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='histo-chart-final') 
        ])
        ])
    ]),
    ]

# Add controls to build the interaction
@callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value'),
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)