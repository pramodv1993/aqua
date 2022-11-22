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
from plotly_wordcloud import plotly_wordcloud


from utils import data

paper_bg_color = '#fafafa'
plot_bg_color='#e8eaef'
def get_empty_graph():
    #empty_graph
    empty_layout = go.Layout(   paper_bgcolor=paper_bg_color,
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
         color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.update_layout(    
    paper_bgcolor=paper_bg_color,
    plot_bgcolor=plot_bg_color)
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
    
    color_scale = 'teal'
    trace1 = go.Heatmap(x=xx[0], y=y_, z=Z,
                colorscale=color_scale,
                showscale=True)
    # fig = io.read_json('boundary.json')
    trace2 = go.Scatter(x=X[:, 0], y=X[:, 1],
                        mode='markers',
                        showlegend=False,
                        marker=dict(size=10,
                                    color=y, 
                                    colorscale=color_scale,
                                    line=dict(color='black', width=1))
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
                fig.add_trace(
                    go.Bar(
                        x=[np.random.rand() for _ in range(num_topics)],
                        y=[f'topic_{i}' for i in range(num_topics)],
                        orientation='h',
                        name=next(dataset)
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
    if lb:
        fig.add_vline(x=lb, line_width=2, line_dash='dash')
    if ub:
        fig.add_vline(x=ub, line_width=2, line_dash='dash')
    fig.update_layout(    
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
            theta=data.bias.columns[1:],
            fill='toself',
            name=name,
    ))
    fig.update_layout(
        width=1000,
        polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )),
        showlegend=True
    )
    globals()['prev_s4_g2'] = fig
 
def update_toxicity_plot(points):
    if points is None:
        return get_empty_graph()
    fig = get_word_cloud("""
    <p>Lorem ipsum dolor sit amet. He freaking place a this moron the idiot moron. 
    The moron this is freaking banished is banished moron be very place. 
    A must hell the stupid must be moron idiot. 
    </p><p>Is banished banished he moron moron be from place is must from be very stupid he must moron was place hell.
     Is stupid this he from place was this freaking is place stupid! </p><p>He stupid place he moron must is this this was moron moron was stupid moron. 
     Bad stupid moron be hell idiot he from place a idiot this. A this moron was moron place be stupid very is hell moron bad stupid must a banished very!
      </p><p>A very this a this place he hell moron be very place. He place from he this freaking he idiot freaking he from stupid the very idiot bad banished 
      this is this idiot. Bad banished must was must place is moron moron he idiot idiot bad place from bad banished from is idiot must. </p>

    """)
    fig.update_layout(title='Topics')
    globals()['prev_s4_g1'] = fig
    
def get_word_cloud(text):
    return plotly_wordcloud(text)