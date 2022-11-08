from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

#@TODO compute metrics for chosen datasets/ chosen points
def get_scatter_plot(selected_datasets):
    if not selected_datasets:
        return get_empty_graph()
    x = np.random.randint(0, 100, size=(100,2))
    labels = selected_datasets
    y = np.array([[np.random.choice(labels)] for _ in range(100)])
    points = pd.DataFrame(np.concatenate((x, y), axis=1), columns=list('ABC'))
    fig = px.scatter(points, x='A', y='B', color='C')
    fig.update_layout(title='Select points')
    return fig

def get_bar_graph(selected_datasets):
    if not selected_datasets:
        return get_empty_graph()
    fig = go.Figure(data=[
        go.Bar(name=dataset, x=['m1', 'm2', 'm3', 'm4'], y = [np.random.randn(20) for _ in range(4)]) for dataset in selected_datasets
    ])
    fig=fig.update_layout(barmode='group')
    return fig

def get_dist_plot(selected_datasets):
    if not selected_datasets:
        return get_empty_graph()
    labels = selected_datasets
    fig = ff.create_distplot([np.random.randn(200) - x for x in range(len(selected_datasets))], selected_datasets)
    return fig

def get_empty_graph():
    #empty_graph
    empty_layout = go.Layout(plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    xaxis = dict(showticklabels=False, showgrid=False, zeroline = False),
    yaxis = dict(showticklabels = False, showgrid=False, zeroline = False),
    height=700, width=700)
    empty_graph = go.Figure()
    # empty_graph.update_layout(empty_layout)
    return empty_graph