from dash import Dash, html, dcc
import plotly.express as px
import plots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='AQuA'),
    dcc.Tabs([
        dcc.Tab(label='Global View', children=[plots.get_scatter_plot()
        ]),
        dcc.Tab(label='Stage I', children=[plots.get_bar_graph()
        ]),
        dcc.Tab(label='Stage II', children=[plots.get_scatter_plot()
        ])
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)