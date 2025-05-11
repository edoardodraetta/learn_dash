"""A dash app with controls, callbacks, and file upload functionality"""
import base64
import io
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dash_table, dcc, html
import dash_bootstrap_components as dbc

# dcc = dash core components

# Incorporate default data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App components to display
app.layout = dbc.Container([
    # Title
    dbc.Row([
        html.Div('My First App with Data, Graph, and Controls', className="text-primary text-center fs-3")
    ]),
    # Upload
    dbc.Row([
        html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select a CSV File')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=False
            ),
            html.Div(id='upload-status')
        ])
    ]),
    dbc.Row([
        dbc.RadioItems(
            options=[{"label": x, "value": x} for x in ["pop", 'lifeExp', 'gdpPercap']],
            value="lifeExp", inline=True, id='radio-buttons-final')
    ]),
    dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    data=df.to_dict('records'), page_size=12, # type: ignore
                    style_table={'overflowX': 'auto'}, id='table-component') 
            ], width=6),

            dbc.Col([
                dcc.Graph(figure={}, id='my-first-graph-final')
            ], width=6),
        ]),

    ], fluid=True)

# Process the uploaded file
@callback(
    Output('table-component', 'data'),
    Output('upload-status', 'children'),
    Input('upload-data', 'contents'),
    prevent_initial_calll=True
)
def update_output(contents):
    if contents is not None:
        df = parse_contents(contents)
        if df is not None:
            return df.to_dict('records'), html.Div('Upload successful!')
        return [], html.Div('Error processing file!', style={'color': 'red'})
    return [], html.Div()

# Parse uploaded file
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decode = base64.b64decode(content_string)
    try:
        # assume that the user uploaded a csv file
        return pd.read_csv(io.StringIO(decode.decode('utf-8')))
    except Exception as e:
        print(e)
        return None


# Add controls to build the interaction
@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value'),
    Input('table-component', 'data')
)
def update_graph(col_chosen, data):
    if not data:  # If no data, use the default dataframe
        dff = df
    else:
        dff = pd.DataFrame(data)
    fig = px.histogram(dff, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)