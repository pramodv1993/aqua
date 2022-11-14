from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import plots
from Constants import Datasets
datasets = [dataset.name for dataset in Datasets]

def _create_slider(stage_num, graph_num, metric_num, div_class=None, div_style=None):
    if not div_class:
        div_class = "pretty_container six columns"
    return html.Div(
                style= div_style,
                children=[
                    html.Br(),
                    html.H4("Select thresholds:"), html.Br(),
                    "Lower bound", html.Br(),\
                    dcc.Input(id=f"stage{stage_num}_g{graph_num}_lower", type="range"),  html.Br(), \
                    "Upper bound", html.Br(),\
                    dcc.Input(id=f"stage{stage_num}_g{graph_num}_upper", type="range")], className=div_class)

def _create_metric_graph(stage_num, graph_num, metric_num):
    return html.Div(children=[                
                    html.Div(children= dcc.Graph(id=f"stage{stage_num}_g{graph_num}"), className='pretty_container six columns')], 
            id=f'metric{metric_num}')

def _create_empty_graph(graph_id, div_id, div_class):
    return html.Div(children=[dcc.Graph(id=graph_id)], id=div_id, className=div_class)

def _create_global_dataselector(datasets):
    return html.Div(style={'marginLeft' : '30px'}, children=[\
                html.Br(),
                html.H4("Select points:"), html.Br(),\
                dcc.Checklist(datasets, value=[], id='dataset_selector')],
                id='checklist_container', className='pretty_container six columns')

def make_layout():
    return html.Div(children=[
    html.H1(children='AQuA'),
    html.H4(children=[html.B('A Qu'), 'ality ', html.B('A'), 'ssistance framework for introspecting your text corpora..']),
    dcc.Tabs([
        #First stage of the pipeline - basic analysis
        dcc.Tab(label='Stage I', children=[
            #config-row 1
            html.Div(children=[
                        _create_global_dataselector(datasets),
                         html.Div(html.H4("Filtered points:"), className="offset-by-six columns"), html.Br()
            ],  className="row"),
            #graphs-row 1
            html.Div([
                html.Div([
                    _create_empty_graph(graph_id='global_view',\
                         div_id="global_view_container", \
                         div_class='pretty_container six columns'),
                #filtered graph
                _create_metric_graph(1, 1, 1),
                html.Div(children=[html.Button("Fix points", id='fixed_points'),\
                html.Button("Reset selection", id='refresh_view')], className="offset-by-six columns")
])        
            ],  className="row"),
            #config-row 2
            html.Div(children=[
                _create_slider(1, 3, 3, div_class="offset-by-six columns"),\
            ],  className="row"),
            #graphs-row 2
            html.Div(children=[
                 html.H4("Composition:"),
                 #composition graph
                _create_metric_graph(1, 2, 2),
                #distribution graph
                _create_metric_graph(1, 3, 3)
            ],  className="row"),
            #config-row 3
            html.Div(children=[
                _create_slider(1, 4, 4)
            ],  className="row"),
            #graphs-row 3
            html.Div(children=[
                _create_metric_graph(1, 4, 4),
            ],  className="row")
        ]),

        #Second stage of the pipeline - deeper analysis
        dcc.Tab(label='Stage II', children=[
            #config-row 1
            html.Div(children=[
                        _create_slider(2, 1, 5),
                        _create_slider(2, 2, 6),
            ],  className="row"),
            #graphs-row 1
            html.Div([
                html.Div([
                    _create_metric_graph(2, 1, 5),
                    _create_metric_graph(2, 2, 6)]),
                    ],  className="row"),
            #config-row 2
            html.Div(children=[
                _create_slider(2, 3, 7),
                _create_slider(2, 4, 8),
            ],  className="row"),
            #graphs-row 2
            html.Div(children=[
                _create_metric_graph(2, 3, 7),
                _create_metric_graph(2, 4, 8),
            ],  className="row")
        ]),

        #Third stage of the pipeline
        dcc.Tab(label='Stage III', children=[
            #config-row 1
            html.Div(children=[
                        _create_slider(3, 1, 9),
                        _create_slider(3, 2, 10),
            ],  className="row"),
            #graphs-row 1
            html.Div([
                html.Div([
                    _create_metric_graph(3, 1, 9),
                    _create_metric_graph(3, 2, 10)]),
                    ],  className="row"),
            #config-row 2
            html.Div(children=[
                _create_slider(3, 3, 11),
                _create_slider(3, 4, 12),
            ],  className="row"),
            #graphs-row 2
            html.Div(children=[
                _create_metric_graph(3, 3, 11),
                _create_metric_graph(3, 4, 12),
            ],  className="row")
        ]),

    ]),
])