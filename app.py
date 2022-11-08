from dash import Dash
from layout import make_layout
from callbacks import define_callbacks


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = make_layout()
define_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)