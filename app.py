"""Hello world dash app"""
from dash import Dash, html

# Initialize the app (the dash constructor)
app = Dash()

# App components to display
app.layout = [html.Div(children='Hello World')]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)