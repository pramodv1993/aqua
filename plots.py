from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np


def get_scatter_plot(datasets):
    if not datasets:
        return get_empty_graph()
    x = np.random.randint(0, 100, size=(100,2))
    labels = datasets
    y = np.array([[np.random.choice(labels)] for _ in range(100)])
    points = pd.DataFrame(np.concatenate((x, y), axis=1), columns=list('ABC'))
    fig = px.scatter(points, x='A', y='B', color='C')
    fig.update_layout(title='Select points')
    return fig

def get_bar_graph():
    fig =  px.bar(x=[1,2], y = [3,4])
    fig.update_layout(title="Metrics")
    return fig


def get_dist_plot():
    fig = ff.create_distplot([np.random.randn(200), np.random.randn(200)-2], ['dataset1', 'dataset2'])
    return fig


def get_empty_graph():
    #empty_graph
    empty_layout = go.Layout(plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    xaxis = dict(showticklabels=False, showgrid=False, zeroline = False),
    yaxis = dict(showticklabels = False, showgrid=False, zeroline = False),
    height=700, width=700)
    empty_graph = go.Figure()
    empty_graph.update_layout(empty_layout)
    return empty_graph