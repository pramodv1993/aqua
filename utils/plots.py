import random
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn import svm
from sklearn.preprocessing import StandardScaler

from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
from plotly import io
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from utils.plotly_wordcloud import plotly_wordcloud
from utils import data
from utils import callbacks

paper_bg_color = '#fafafa'
plot_bg_color='#e8eaef'
color_discrete_map={
            'DATASET_1':'rgb(229, 134, 6)',
            'DATASET_2':'rgb(93, 105, 177)',
            'DATASET_3':'rgb(82, 188, 163)',
             'DATASET_4':'rgb(153, 201, 69)'}
def get_empty_graph(width=None, height=None):
    #empty_graph
    empty_layout = go.Layout(   
    paper_bgcolor=paper_bg_color,
    plot_bgcolor=plot_bg_color,
    xaxis = dict(showticklabels=True, showgrid=True, zeroline = True),
    yaxis = dict(showticklabels = True, showgrid=True, zeroline = True))
    empty_graph = go.Figure()
    empty_graph.update_layout(empty_layout)
    return empty_graph

#stage1 graphs
prev_s1_g1 = get_empty_graph()
prev_s1_g3 = get_empty_graph()
prev_s1_g2 = get_empty_graph()
prev_s1_g4 = get_empty_graph()
prev_s1_g5 = get_empty_graph()
prev_s1_g6 = get_empty_graph()
prev_s1_g7 = get_empty_graph()
prev_s1_g8 = get_empty_graph()
prev_s1_g9 = get_empty_graph()
#stage2 graphs
prev_s2_g1 = get_empty_graph()
prev_s2_g3 = get_empty_graph()
prev_s2_g2 = get_empty_graph()
prev_s2_g4 = get_empty_graph()
#stage3 graphs
prev_s3_g1 = get_empty_graph()
prev_s3_g2 = get_empty_graph()
#stage4 graphs
prev_s4_g1 = get_empty_graph()
prev_s4_g2 = get_empty_graph()

def reset_graphs(stage_nums=None):
    if stage_nums:
        for stage_num in stage_nums:
            for graph_num, metric in data.stage_vs_metrics[stage_num].items():
                globals()[f'prev_s{stage_num}_g{graph_num}'] = get_empty_graph()

def update_dist_plots_for_stage(points, stage_nums=None, ub=None, lb=None):
    if stage_nums:
        for stage_num in stage_nums:
            for graph_num, metric in data.stage_vs_metrics[stage_num].items():
                #ignore stages and plots that isnt a distribution
                if (stage_num==1 and graph_num==2) or (stage_num in [3,4]):
                    continue
                globals()[f'prev_s{stage_num}_g{graph_num}'] = get_dist_plot(points, lb, ub, metric)

def get_scatter_plot(points):
    if points is None:
        return get_empty_graph()
    fig = px.scatter(points, x='pc1', y='pc2', color='name', hover_data=['id'],\
         color_discrete_map=color_discrete_map)
    fig.update_layout(    
    paper_bgcolor=paper_bg_color,
    plot_bgcolor=plot_bg_color)
    fig.update_xaxes(range=[-7,7])
    fig.update_yaxes(range=[-7,7])
    return fig

def update_classifier_plot(points):
    h = .5
    if points is None:
        return get_empty_graph()
    #generate dummy labels for selected points
    X, y = np.array(pd.concat([points.pc1, points.pc2], axis=1)), np.array([np.random.randint(2) for _ in range(points.shape[0])])
    y_conf = np.array([np.random.rand() for _ in range(points.shape[0])])
    X = StandardScaler().fit_transform(X)
    trees = RandomForestClassifier(max_depth=10,\
                                   n_estimators=10)
    # trees = AdaBoostClassifier()
    trees.fit(X, y)
    #get predictions for entire grid to plot heatmap
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h)
                    , np.arange(y_min, y_max, h))
    y_ = np.arange(y_min, y_max, h)
    Z = trees.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    color_scale = 'aggrnyl'
    trace1 = go.Heatmap(x=xx[0], y=y_, z=Z,
                colorscale=color_scale,
                showscale=True)
    # fig = io.read_json('boundary.json')
    trace2 = go.Scatter(x=X[:, 0], y=X[:, 1],
                        mode='markers',
                        showlegend=False,
                        marker=dict(size=7,
                                    color=y, 
                                    colorscale=color_scale,
                                    line=dict(color='black', width=.6))
                        )
    layout= go.Layout(
            autosize= True,
            title= 'Random Forest (1: Higher Quality)',
            hovermode= 'closest',
            showlegend= False,
            paper_bgcolor=paper_bg_color,
            plot_bgcolor=plot_bg_color)
    fig = go.Figure(data = [trace1, trace2], layout=layout) 
    globals()['prev_s3_g1'] = fig


def update_topics_plot(points):
    datasets = points.name.unique()
    num_datasets = len(datasets)
    num_topics = 10
    num_rows = (num_datasets//2 + num_datasets%2)
    fig = make_subplots(rows=num_rows, cols=2)
    dataset = iter(datasets)
    for i in range(1, num_rows+1):
        try:
            for j in range(1, 3):
                name =next(dataset)
                fig.add_trace(
                    go.Bar(
                        x=[np.random.rand() for _ in range(num_topics)],
                        y=[f'topic_{i}' for i in range(num_topics)],
                        orientation='h',
                        name=name,
                        marker_color=color_discrete_map[name]
                        ),
                row=i, col=j
                )
        except:
            break
    fig.update_layout(bargap=0.17,
         width=1000,
         height=600,
         paper_bgcolor=paper_bg_color,
         plot_bgcolor=plot_bg_color)
    globals()['prev_s3_g2']= fig

def get_bar_graph(selected_datasets=None):
    if not selected_datasets:
        return get_empty_graph()
    fig = go.Figure(data=[
        go.Bar(name=dataset, x=['m1', 'm2', 'm3', 'm4'],\
             y = [np.random.randn(20) for _ in range(4)]) for dataset in selected_datasets
    ])
    fig.update_layout(    
    barmode='group',
    paper_bgcolor=paper_bg_color,
    plot_bgcolor=plot_bg_color)
    return fig

def get_dist_plot(points, lb=None, ub=None, metric=None):
    if points is None:
        return get_empty_graph()
    metrics_for_points = data.get_metrics_for_points(points.id)
    fig = px.histogram(metrics_for_points, x=metric, marginal='box', color='name', color_discrete_sequence=px.colors.qualitative.Vivid)
    prev_lb, prev_ub = data.metrics_vs_bounds[metric]
    if lb: 
        fig.add_vline(x=lb, line_width=2, line_dash='dash')
        #persist bound for metric for final filtering
        data.metrics_vs_bounds[metric] = (lb, prev_ub)
        prev_lb = lb
    if ub:
        fig.add_vline(x=ub, line_width=2, line_dash='dash')
        data.metrics_vs_bounds[metric] = (prev_lb, ub)
    fig.update_layout(
    font=dict(size=20),   
    paper_bgcolor=paper_bg_color,
    plot_bgcolor=plot_bg_color)
    return fig

def _build_tree_map(dataset):
    fig = px.treemap(dataset, path=[px.Constant("all"), 'lang', 'name'], values='count')
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25),
    paper_bgcolor=paper_bg_color,
    plot_bgcolor=plot_bg_color)
    return fig

def get_data_composition_graph(points=None):
    if points is None:
        return get_empty_graph()
    return _build_tree_map(points)

def update_bias_plot(points):
    if points is None:
        return get_empty_graph()
    datasets = points.name.unique()
    fig = go.Figure()
    for name in datasets:
        fig.add_trace(go.Scatterpolar(
            r=data.get_bias_info_for_dataset(name),
            theta=data.bias.columns[2:],
            fill='toself',
            name=name,
    ))
    fig.update_layout(
        title='1.0: Biased',
        width=10000,
        font=dict(size=17),
        polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )),
        showlegend=True
    )
    globals()['prev_s4_g2'] = fig
 

def update_topic_words_plot(points):
    if points is None:
        return get_empty_graph()
    print(points)
    import random
    fig, words = get_word_cloud(
    '''It is a long established fact that a reader will be distracted by 
            the readable content of a page when looking at its layout. The point of using 
            Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 
            'Content here, content here', making it look like readable English.Various versions have evolved over the years, 
            sometimes by accident, sometimes on purpose (injected humour and the like).''')
    # fig.update_layout(title='Words in Topic')
    words = random.sample(words, np.random.randint(len(words)))
    print(words)
    fig = go.Figure(data=[go.Table(
            # columnorder = [1,2],
            columnwidth = [40],
            header = dict(
                values = [['Words']],
                line_color='darkslategray',
                fill_color='grey',
                align=['center'],
                font=dict(color='white', size=25),
                height=40
            ),
            cells=dict(
                values=[words],
                line_color='darkslategray',
                fill=dict(color=['white']),
                align=['center'],
                font_size=20,
                height=40)
                )
            ])
    fig.update_layout(
        title='Words in Topic',
             width=600,
    height=1500)
    return fig

def update_toxicity_plot(points):
    if points is None:
        return get_empty_graph()
    toxic_words = data.get_toxic_words_for_points(points)
    fig = go.Figure(data=[go.Table(
            columnorder = [1,2],
            columnwidth = [40,40],
            header = dict(
                values = [['Words'],
                            ['ConfidenceScores']],
                # line_color='darkslategray',
                fill_color='grey',
                align=['center','center'],
                font=dict(color='white', size=25),
                height=40
            ),
            cells=dict(
                values=[toxic_words.word, toxic_words.score],
                line_color='darkslategray',
                fill=dict(color=['white', 'white']),
                align=['center', 'center'],
                font_size=20,
                height=40)
                )
            ])
    fig.update_layout(
             width=900,
    height=1500)
    globals()['prev_s4_g1'] = fig
    
def get_word_cloud(text):
    return plotly_wordcloud(text)

#@TODO table view of corpus