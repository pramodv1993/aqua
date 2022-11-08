from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import plots
from Constants import Datasets
datasets = [dataset.name for dataset in Datasets]

def make_layout():
    return html.Div(children=[
    html.H1(children='AQuA'),
    html.H4(children="One stop shop for introspecting your corpora.."),
    dcc.Tabs([
        dcc.Tab(label='Stage I', children=[
            html.Div([
                html.Div([
                    html.Div([dcc.Checklist(datasets, value=[], id='dataset_selector')],
                            id='checklist'),
                    html.Div(children= [dcc.Graph(id='global_view')], id='global_view_container')
                    ], className='pretty_container six columns')
            ],  className="row")
        ]),
        dcc.Tab(label='Stage II', children=[
            html.Div(children=[
                dcc.Graph(figure=plots.get_bar_graph())], className='pretty_containier six columns'
            )
        ]),
        dcc.Tab(label='Stage III', children=[
            html.Div(children=[
                dcc.Graph(figure=plots.get_dist_plot())], className='pretty_container six columns')
        ])
    ]),
])