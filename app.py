"""A dash app with controls, callbacks, file upload, and storage functionality with clickable files"""
import base64

# import io
import os
from datetime import datetime

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import ALL, Dash, Input, Output, State, callback, ctx, dash_table, dcc, html, no_update

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Set default dataframe - will be replaced when file is uploaded
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Create a data directory if it doesn't exist
UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# App components to display
app.layout = dbc.Container([
    dbc.Row([
        html.Div('My First App with Data Upload, Storage, Graph, and Controls', className="text-primary text-center fs-3")
    ]),
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
                multiple=False
            ),
            html.Div(id='upload-status')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H5("Stored Files:"),
            html.Div(id='file-list', style={'marginBottom': '20px'})
        ])
    ]),
    dbc.Row([
        dbc.RadioItems(
            options=[{"label": x, "value": x} for x in ["pop", 'lifeExp', 'gdpPercap']],
            value="lifeExp", inline=True, id='radio-buttons-final')
    ]),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=12,  # type: ignore
                                style_table={'overflowX': 'auto'},
                                id='table-component')
        ], width=6),
        dbc.Col([
            dcc.Graph(figure={}, id='my-first-graph-final')
        ], width=6),
    ]),
    # Hidden div to store current filename
    html.Div(id='current-filename', style={'display': 'none'})
], fluid=True)

# Save uploaded file to directory and return the dataframe
def save_file(content, filename):
    content_type, content_string = content.split(',')
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

# Get list of files in the uploads directory
def get_file_list():
    if not os.path.exists(UPLOAD_DIRECTORY):
        return []
    return sorted([f for f in os.listdir(UPLOAD_DIRECTORY) if not f.startswith('.')])

# Create clickable file list items
def create_file_list_ui():
    files = get_file_list()
    if not files:
        return html.Div("No files uploaded yet")
    
    return html.Ul([
        html.Li([
            html.Button(
                file,
                id={'type': 'file-button', 'index': i},
                style={
                    'background': 'none',
                    'border': 'none',
                    'color': '#007bff',
                    'textDecoration': 'underline',
                    'cursor': 'pointer',
                    'padding': '5px 0'
                }
            )
        ]) for i, file in enumerate(files)
    ], style={'listStyleType': 'none', 'padding': '0'})

# Load a file from storage
def load_file_from_storage(filename):
    filepath = os.path.join(UPLOAD_DIRECTORY, filename)
    try:
        if filename.endswith('.csv'):
            return pd.read_csv(filepath), None
        else:
            return None, "Only CSV files are supported for visualization"
    except Exception as e:
        return None, str(e)

# Callback to process uploaded file
@callback(
    Output('table-component', 'data'),
    Output('upload-status', 'children'),
    Output('file-list', 'children'),
    Output('current-filename', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def update_output(contents, filename):
    if contents is not None:
        df, saved_filename, error = save_file(contents, filename)
        
        # Update file list
        file_list = create_file_list_ui()
        
        if error:
            return [], html.Div(f'Error: {error}', style={'color': 'red'}), file_list, ""
        
        if df is not None:
            return df.to_dict('records'), html.Div([
                f'File "{filename}" uploaded and saved as "{saved_filename}"'
            ], style={'color': 'green'}), file_list, saved_filename
        
    # Default return if no file is uploaded
    file_list = create_file_list_ui()
    return [], html.Div(), file_list, ""

# Callback for clicking on a file in the list
@callback(
    Output('table-component', 'data', allow_duplicate=True),
    Output('upload-status', 'children', allow_duplicate=True),
    Output('current-filename', 'children', allow_duplicate=True),
    Input({'type': 'file-button', 'index': ALL}, 'n_clicks'),
    State('file-list', 'children'),
    prevent_initial_call=True
)
def load_selected_file(n_clicks, file_list):
    # Check if any button was clicked
    if not any(click for click in n_clicks if click):
        return no_update, no_update, no_update
    
    # Find which button was clicked
    button_id = ctx.triggered_id
    if button_id is None:
        return no_update, no_update, no_update
    
    # Get the index of the clicked button
    clicked_index = button_id['index']
    
    # Get the list of files
    files = get_file_list()
    if clicked_index >= len(files):
        return no_update, no_update, no_update
    
    # Get the filename
    filename = files[clicked_index]
    
    # Load the file
    df, error = load_file_from_storage(filename)
    
    if error:
        return [], html.Div(f'Error loading file: {error}', style={'color': 'red'}), ""
    
    if df is not None:
        return df.to_dict('records'), html.Div(f'Loaded file: {filename}', style={'color': 'green'}), filename
    
    return no_update, no_update, no_update

# Graph update callback
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
    
    # Check if necessary columns exist
    if 'continent' in dff.columns and col_chosen in dff.columns:
        fig = px.histogram(dff, x='continent', y=col_chosen, histfunc='avg')
    else:
        # Create an empty figure with a message if columns don't exist
        fig = px.histogram()
        fig.update_layout(
            title="Upload data with 'continent' and selected column to display graph"
        )
    return fig

# Initialize the app
@app.callback(
    Output('file-list', 'children', allow_duplicate=True),
    Input('file-list', 'id'),
    prevent_initial_call='initial_duplicate'
)
def initialize_file_list(id):
    return create_file_list_ui()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)