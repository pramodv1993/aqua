from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

dataset = pd.read_csv('datasets/dataset.csv')
metrics = pd.read_csv('datasets/metrics.csv')
names = dataset.name.unique()

def get_scatter_plot(selected_datasets=None, ids=None):
    if not selected_datasets and not ids:
        return get_empty_graph()
    filtered = None
    if selected_datasets:
        filtered = dataset[dataset.name.isin(selected_datasets)]
    if ids:
        if filtered:
            filtered = filtered[filtered.id.isin(ids)]
        else:
            filtered = dataset[dataset.id.isin(ids)]
    fig = px.scatter(filtered, x='pc1', y='pc2', color='name', hover_data=['id'])
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

def get_dist_plot(ids):
    if not ids:
        return get_empty_graph()
    fig = ff.create_distplot([np.random.randn(200) - x for x in range(len(names))], names)
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