from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import plots
from Constants import Datasets
datasets = [dataset.name for dataset in Datasets]

def make_layout():
    return html.Div(children=[
    html.H1(children='AQuA'),
    html.H4(children="Framework for introspecting your corpora.."),
    dcc.Tabs([
        dcc.Tab(label='Stage I', children=[
            html.Div([
                html.Div([
                    html.Div([dcc.Checklist(datasets, value=[], id='dataset_selector')],
                            id='checklist'),
                    html.Div(children= dcc.Graph(id='global_view'), id='global_view_container')
                    ], className='pretty_container six columns'),
                html.Div(children= dcc.Graph(id='stagei_g1'), className='pretty_container six columns'),
            ],  className="row"),
            html.Div([
                html.Div(children= dcc.Graph(id='stagei_g2'), className='pretty_container six columns'),
                html.Div(children= dcc.Graph(id='stagei_g3'), className='pretty_container six columns'),
            ],  className="row")
        ]),
        dcc.Tab(label='Stage II', children=[
            html.Div([
                html.Div(children=dcc.Graph(id='stageii_g1'), className='pretty_containier six columns'),
                html.Div(children=dcc.Graph(id='stageii_g2'), className='pretty_containier six columns')
            ], className='row'),
            html.Div([
                html.Div(children=dcc.Graph(id='stageii_g3'), className='pretty_containier six columns'),
                html.Div(children=dcc.Graph(id='stageii_g4'), className='pretty_containier six columns')
            ], className='row')
        ]),
        dcc.Tab(label='Stage III', children=[
            html.Div([
                html.Div(children=dcc.Graph(id='stageiii_g1'), className='pretty_containier six columns'),
                html.Div(children=dcc.Graph(id='stageiii_g2'), className='pretty_containier six columns')
            ], className='row'),
            html.Div([
                html.Div(children=dcc.Graph(id='stageiii_g3'), className='pretty_containier six columns'),
                html.Div(children=dcc.Graph(id='stageiii_g4'), className='pretty_containier six columns')
            ], className='row')
        ]),

    ]),
])