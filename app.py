"""A dash app with controls, callbacks, file upload, and storage functionality"""
import base64
import io
import os
from datetime import datetime

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dash_table, dcc, html, State

# Incorporate default data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Create a data directory if it doesn't exist
UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

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
    # Uploaded files
    dbc.Row([
        dbc.Col([
            html.H5("Stored Files:"),
            html.Ul(id='file-list')
        ])
    ]),

    # Radio button
    dbc.Row([
        dbc.RadioItems(
            options=[{"label": x, "value": x} for x in ["pop", 'lifeExp', 'gdpPercap']],
            value="lifeExp", inline=True, id='radio-buttons-final')
    ]),

    # Table and chart
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
    Output('file-list', 'children'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    prevent_initial_calll=True
)
def update_output(contents, filename):
    if contents is not None:
        df, saved_filename, error = save_file(contents, filename)
        
        # Update file list
        files = get_file_list()
        file_list = [html.Li(file) for file in files]

        if error:
            return [], html.Div(f'Error: {error}', style={'color': 'red'}), file_list
        
        if df is not None:
            return df.to_dict('records'), html.Div([
                f'File "{filename}" uploaded and saved as "{saved_filename}"'
            ]), file_list
        
    # Default return if no file is uploaded
    files = get_file_list()
    file_list = [html.Li(file) for file in files]
    return [], html.Div(), file_list

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

# Save uploaded file
def save_file(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    clean_filename = ''.join(c if c.isalnum() or c in ['.', '-', '_'] else '_' for c in filename)
    safe_filename = f"{timestamp}_{clean_filename}"
    filepath = os.path.join(UPLOAD_DIRECTORY, safe_filename)

    try:
        # Save file to uploads directory
        with open(filepath, "wb") as f:
            f.write(decoded)
        
        # Read file back as dataframe
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
            return df, safe_filename, None
        else:
            return None, safe_filename, "Only CSV files are supported for visualization"
    except Exception as e:
        return None, None, str(e)

# Load file from storage
@callback(
    Output('table-component', 'data', allow_duplicate=True),
    Output('upload-status', 'children', allow_duplicate=True),
    Input('file-list', 'children'),
    State('file-list', 'children'),
    prevent_initial_call=True
)
def load_file(n_clicks, file_list):
    # This is a simplified version - clicking on the file list would load the file
    # In a real app, you'd want to have clickable file names or buttons
    
    # For now, just show a message
    return [], html.Div("Click on a file to load it (functionality not implemented in this example)")


# Get list of files in the uploads directory
def get_file_list():
    if not os.path.exists(UPLOAD_DIRECTORY):
        return []
    return sorted([f for f in os.listdir(UPLOAD_DIRECTORY) if not f.startswith('.')])

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