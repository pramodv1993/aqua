from dash import Dash
from layout import make_layout
from callbacks import define_callbacks
import dash_bootstrap_components as dbc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=[external_stylesheets, dbc.themes.BOOTSTRAP])
app.layout = make_layout()
define_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)