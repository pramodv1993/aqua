from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import plots
from Constants import Datasets
from utils import data
datasets = [dataset.name for dataset in Datasets]

def _create_range_slider(stage_num,\
    graph_num,\
    metric_num,\
    div_class=None,\
    div_style=None,\
    title=None,\
    max_r=100):
    if not title:
        title="Select thresholds:"
    if not div_class:
        div_class = "pretty_container six columns"
    return html.Div(
                style= div_style,
                children=[
                    html.Br(),
                    html.H4(title),
                    html.H4("Select Thresholds:"), html.Br(),\
                    dcc.RangeSlider(0,max_r, id=f"stage{stage_num}_g{graph_num}_range"),  html.Br(),
                    html.Div(id=f"stage{stage_num}_g{graph_num}_selected_range")
                    ], \
                    className=div_class)

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
            
            #graphs-row 2
            html.Div(children=[
                 html.Div(children=[\
                    _create_range_slider(1, 3, 3,\
                        max_r=data.metrics.total_words_per_doc.max(),\
                        title='#words / doc')], className="offset-by-six columns"),
                 #composition graph
                 html.H4("Composition:"),
                _create_metric_graph(1, 2, 2),
                #words/doc graph
                _create_metric_graph(1, 3, 3)
            ],  className="row"),
            
            #config-row 3
            html.Div(children=[
                _create_range_slider(1, 4, 4,\
                    max_r=data.metrics.avg_word_length.max(),
                    title="avg word lengths"),
                 _create_range_slider(1, 5, 5,\
                    max_r=data.metrics.total_num_sent.max(),
                    title="#sentences / doc")
            ],  className="row"),
            #graphs-row 3
            html.Div(children=[
                #avg_word_length graph
                _create_metric_graph(1, 4, 4),
                #sentences / doc
                _create_metric_graph(1, 5, 5)
            ],  className="row"),

            #config-row 4
            html.Div(children=[
                _create_range_slider(1, 6, 6,\
                    max_r=data.metrics.avg_sent_length.max(), title="avg sent lengths"),
                 _create_range_slider(1, 7, 7,\
                    max_r=data.metrics.token_type_ratio.max(), title="token type ratio")
            ],  className="row"),
            #graphs-row 4
            html.Div(children=[
                #avg sent lengths graph
                _create_metric_graph(1, 6, 6),
                #token type ratio graph
                _create_metric_graph(1, 7, 7)
            ],  className="row"),

            #config-row 5
            html.Div(children=[
                _create_range_slider(1, 8, 8,\
                    max_r=data.metrics.symbol_word_ratio.max(), title="symbol-word ratio"),
                 _create_range_slider(1, 9, 9,\
                    max_r=data.metrics.num_non_alphabet_words.max(), title="#non-alphabet words")
            ],  className="row"),
            #graphs-row 4
            html.Div(children=[
                #symbol-word ratio graph
                _create_metric_graph(1, 8, 8),
                #non-alphabet words graph
                _create_metric_graph(1, 9, 9)
            ],  className="row"),
            
        ]),

        #Second stage of the pipeline - deeper analysis
        dcc.Tab(label='Stage II', children=[
            #config-row 1
            html.Div(children=[
                        _create_range_slider(2, 1, 10, title="% of stop words "),
                        _create_range_slider(2, 2, 11, title="% of abbreviations"),
            ],  className="row"),
            #graphs-row 1
            html.Div([
                html.Div([
                    _create_metric_graph(2, 1, 10),
                    _create_metric_graph(2, 2, 11)]),
                    ],  className="row"),
            #config-row 2
            html.Div(children=[
                _create_range_slider(2, 3, 12, title="# of exact duplicates"),
                _create_range_slider(2, 4, 13, title="# of near duplicates"),
            ],  className="row"),
            #graphs-row 2
            html.Div(children=[
                _create_metric_graph(2, 3, 12),
                _create_metric_graph(2, 4, 13),
            ],  className="row")
        ]),

        #Third stage of the pipeline
        dcc.Tab(label='Stage III', children=[
            #config-row 1
            html.Div(children=[
                        _create_range_slider(3, 1, 14, title="Topics distribution"),
                        _create_range_slider(3, 2, 15, "classifier quality distribution"),
            ],  className="row"),
            #graphs-row 1
            html.Div([
                html.Div([
                    _create_metric_graph(3, 1, 14),
                    _create_metric_graph(3, 2, 15)]),
                    ],  className="row")
        ]),

    ]),
])