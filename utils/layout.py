import base64
import dash
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

from utils.Constants import Datasets
from utils import data
datasets = [dataset.name for dataset in Datasets]

def _create_range_slider(stage_num,\
    graph_num,\
    metric_num,\
    div_style=None,\
    title=None,\
    max_r=100):
    if not title:
        title="Select thresholds:"
    return html.Div(
                style= div_style,
                children=[
                    html.Br(),
                    html.H2(title),
                    html.H4("Select Thresholds:"), html.Br(),\
                    dcc.RangeSlider(-1, max_r, id=f"stage{stage_num}_g{graph_num}_range"),  html.Br(),
                    html.Div(id=f"stage{stage_num}_g{graph_num}_selected_range")
                    ])

def _create_metric_graph(stage_num, graph_num, metric_num, title=None):
    return html.Div(children=[  
                    # dbc.Label(title),              
                    html.Div(children= dcc.Graph(id=f"stage{stage_num}_g{graph_num}"), className='pretty_container six columns')], 
            id=f'metric{metric_num}')

def _create_empty_graph(graph_id):
    return dcc.Graph(id=graph_id)

def _create_global_dataselector(datasets):
    return html.Div(style={'marginLeft' : '30px'}, children=[\
                html.Br(),
                html.Div([
                        dbc.Row(dbc.Label("Embedding model:")),
                        dbc.Row(dcc.Dropdown(['T5', 'RoBERTa', 'DistillBERT'], id='embed')),
                        dbc.Row(dbc.Label("Dim Reduction approach:")),
                        dbc.Row(dcc.Dropdown(['PCA', 'MDS', 'UMAP', 't-SNE'], id='dimred')),
                ]),
                dbc.Row(dbc.Label("Datasets:")),\
                dbc.Row(dbc.Checklist(
                    options=[{"label": f"{dataset}", "value": dataset} for dataset in datasets], 
                    value=[],
                    id='dataset_selector')
                )],
                id='checklist_container', className='pretty_container six columns')

# Using base64 encoding and decoding
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

def create_modal():
    return html.Div(
    [
        dbc.Col(dbc.Button("Framework",
                    id="pipeline",
                    n_clicks=0,
                    className="me-1",
                    size='sm',
                    color='primary',
                    outline=True),
                width={"offset": 6}),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Quality Analysis Pipeline")),
                dbc.Row(html.Img(src=b64_image('utils/pipeline.jpg'), width=3100)),
                # dbc.ModalBody("This is the content of the modal"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_modal", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            size="lg",
            id="my_modal",
            is_open=False,
        ),
    ]
)

def make_layout():
    return html.Div(children=[
    html.Div(id='hidden_div', style={'display': None}),
    dcc.Download(id="export_dataset_download"),
    dcc.ConfirmDialog(id='export_dialog'),
    dbc.Row(dbc.Container([
        html.P(),
        dbc.Row(dbc.Col(html.H2('AQuA'))),
        html.Hr(className="my-1"),
        dbc.Row([
            dbc.Col(html.P([html.B('A Qu'), 'ality ', html.B('A'), 'ssistance framework for introspecting and curating your text corpora..'])),
            # dbc.Col(create_modal(), md=4)
        ]),
    ]), style={'align': 'left', 'margin-left' : '22px'}),
    dbc.Tabs([
        #First stage of the pipeline - basic analysis
        dbc.Tab(tab_id="stage1_tab", label='Stage I', children=[
            #config-row 1
            dbc.Row(children=[
                        dbc.Col(_create_global_dataselector(datasets), md=4),
            ]),
            html.P(),
            dbc.Row([
                dbc.Col(html.H2("Semantic Overview"), style={'align': 'left', 'margin-left' : '22px'}),
                dbc.Col(html.H2("Filtered points"))
            ]),
            #graphs-row 1
            dbc.Row([
                    dbc.Col(_create_empty_graph(graph_id='global_view'), xl=6),
                    dbc.Col([
                        #filtered graph
                        _create_metric_graph(1, 1, 1),
                        dbc.Row([
                            dbc.Col(dbc.Button("Fix points",
                                        id='fixed_points',
                                        className="me-1", 
                                        color='primary',
                                        outline=True),
                                    width={"offset": 2}),
                            dbc.Col(dbc.Button("Reset selection",
                                        id='refresh_view',
                                        className="me-1",
                                        color='primary',
                                        outline=True))
                        ],  className="g-0")
                    ], xl=6)
            ]),
            
            #graphs-row 2
            dbc.Row([
                dbc.Col(_create_range_slider(1, 3, 3,\
                            max_r=data.metrics.total_words_per_doc.max()+1,
                            title='#words / doc'), width={"offset": 6}),
                dbc.Row(html.H2("Composition"), style={'align': 'left', 'margin-left' : '22px'}),
                dbc.Row([
                    #composition graph
                    dbc.Col(_create_metric_graph(1, 2, 2), xl=6),
                    #words/doc graph
                    dbc.Col( _create_metric_graph(1, 3, 3), xl=6)
                ])
            ]),
            html.P(),
            #config-row 3
            dbc.Row([
                dbc.Col(_create_range_slider(1, 4, 4,\
                            max_r=data.metrics.avg_word_length.max()+1,
                            title="Avg Word Lengths"),style={'align': 'left', 'margin-left' : '22px'}),
                dbc.Col(_create_range_slider(1, 5, 5,\
                            max_r=data.metrics.total_num_sent.max()+1,
                            title="#sentences / doc"))
            ]),
            #graphs-row 3
            dbc.Row([
                    #avg_word_length graph
                    dbc.Col(_create_metric_graph(1, 4, 4), xl=6),
                    #sentences / doc graph
                    dbc.Col(_create_metric_graph(1, 5, 5), xl=6)
            ]),
            html.P(),

            #config-row 4
            dbc.Row([
                dbc.Col(_create_range_slider(1, 6, 6,\
                            max_r=data.metrics.avg_sent_length.max()+1,
                            title="Avg Sent Lengths"), style={'align': 'left', 'margin-left' : '22px'}),
                dbc.Col(_create_range_slider(1, 7, 7,\
                            max_r=data.metrics.token_type_ratio.max()+1,
                            title="Token Type Ratio"))
            ]),
            #graphs-row 4
            dbc.Row([
                #avg sent lengths graph
                dbc.Col(_create_metric_graph(1, 6, 6),xl=6),
                #token type ratio graph
                dbc.Col(_create_metric_graph(1, 7, 7), xl=6)
            ]),
            html.P(),

            #config-row 5
            dbc.Row([
                dbc.Col(_create_range_slider(1, 8, 8,\
                            max_r=data.metrics.symbol_word_ratio.max()+1,
                            title="symbol-word ratio"), style={'align': 'left', 'margin-left' : '22px'}),
                dbc.Col(_create_range_slider(1, 9, 9,\
                            max_r=data.metrics.num_non_alphabet_words.max()+1,
                            title="#non-alphabet words"))
            ]),
        
            #graphs-row 6
            dbc.Row([
                #symbol-word ratio graph
                dbc.Col(_create_metric_graph(1, 8, 8),  xl=6),
                #non-alphabet words graph
                dbc.Col(_create_metric_graph(1, 9, 9), xl=6)
            ]),
            html.Br(),
            dbc.Row(
                dbc.Col([
                    dbc.Button("Export Snapshot", color='primary',
                                 outline=True, id='export_dataset_s1'),
                    dbc.Button("Trigger StageII", color='primary',
                                 outline=True, id='stage2_trigger'),
                    dcc.ConfirmDialog(
                            message="Please navigate to StageII tab",
                            id="stage2_alert"),
                    ], width={"offset":5}, xl=5),
                align='center')
        ]),

        #Second stage of the pipeline - deeper analysis
        dbc.Tab(tab_id='stage2_tab', label='Stage II', children=[
            html.P(),
            #config-row 1
            dbc.Row([
                dbc.Col(_create_range_slider(2, 1, 10,\
                            max_r=data.metrics.num_stopwords_per_doc.max()+1,
                            title="#stop words/doc"),style={'align': 'left', 'margin-left' : '22px'}),
                dbc.Col(_create_range_slider(2, 2, 11,\
                            max_r=data.metrics.num_abbreviations_per_doc.max()+1,
                            title="#abbreviations / doc"))
            ]),
            #graphs-row 1
            dbc.Row([
                    #avg_word_length graph
                    dbc.Col(_create_metric_graph(2, 1, 10),  xl=6),
                    #sentences / doc graph
                    dbc.Col(_create_metric_graph(2, 2, 11),  xl=6)
            ]),
            #config-row 2
            dbc.Row([
                dbc.Col(_create_range_slider(2, 3, 12,\
                            max_r=data.metrics.num_exact_duplicates.max()+1,
                            title="# of exact duplicates"), style={'align': 'left', 'margin-left' : '22px'}),
                dbc.Col(_create_range_slider(2, 4, 13,\
                            max_r=data.metrics.num_near_duplicates.max()+1,
                            title="# of near duplicates"))
            ]),
            #graphs-row 2
            dbc.Row([
                # of exact duplicates graph
                dbc.Col(_create_metric_graph(2, 3, 12),  xl=6),
                # of near duplicates graph
                dbc.Col(_create_metric_graph(2, 4, 13),  xl=6)
            ]),
            html.Br(),
            dbc.Row(
                dbc.Col([
                    dbc.Button("Export Snapshot", color='primary',
                                 outline=True, id='export_dataset_s2'),
                    dbc.Button("Trigger StageIII", color='primary',
                                 outline=True, id='stage3_trigger'),
                    dcc.ConfirmDialog(
                            message="Please navigate to StageIII tab",
                            id="stage3_alert"),
                    ], width={"offset":5}, xl=5),
                align='center')
        ]),

        #Third stage of the pipeline
        dbc.Tab(tab_id='stage3_tab', label='Stage III', children=[
            html.P(),
            #config-row 1
            dbc.Row(children=[
                        dbc.Col(html.H2("Classifier Analysis"), style={'align': 'left', 'margin-left' : '22px'}),
                        dbc.Col(html.H2("Topics distributions")),
            ]),
            #graphs-row 1
            dbc.Row([
                #symbol-word ratio graph
                dbc.Col(_create_metric_graph(3, 1, 14),  xl=6),
                #non-alphabet words graph
                dbc.Col(_create_metric_graph(3, 2, 15), xl=6)
            ]),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id='words_in_topic'), xl=6, width={'offset':3})
                ]
            ),
            dbc.Row(
                dbc.Col([
                    dbc.Button("Export Snapshot", color='primary',
                                 outline=True, id='export_dataset_s3'),
                    dbc.Button("Trigger StageIV", color='primary',
                                 outline=True, id='stage4_trigger'),
                    dcc.ConfirmDialog(
                            message="Please navigate to StageIV tab",
                            id="stage4_alert"),

                    ], width={"offset":5}, xl=5),
                align='center')
        ]),

        #Forth stage of the pipeline
        dbc.Tab(tab_id='stage4_tab', label='Stage IV', children=[
            html.P(),
            #config-row 1
            dbc.Row(children=[
                        dbc.Col(html.H2("Toxicity"), style={'align': 'left', 'margin-left' : '22px'}),
                        dbc.Col(html.H2("Bias")),
            ]),
            #graphs-row 1
            dbc.Row([
                #toxicity graph
                dbc.Col(_create_metric_graph(4, 1, 16),  xl=6),
                #bias graph
                dbc.Col(_create_metric_graph(4, 2, 17), xl=6)
            ]),
            html.Br(),
            dbc.Row(
                dbc.Col([
                    dbc.Button("Export Snapshot", color='primary',
                                 outline=True, id='export_dataset_s4'),
                    ], width={"offset":5}, xl=5),
                align='center')
        ]),

    ], 
    active_tab="stage1_tab",
    id='tabs'),
])
