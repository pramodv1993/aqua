from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

from utils import data

def get_scatter_plot(points):
    if points is None:
        return get_empty_graph()
    fig = px.scatter(points, x='pc1', y='pc2', color='name', hover_data=['id'])
    return fig

def get_bar_graph(selected_datasets=None):
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
    fig = ff.create_distplot([np.random.randn(200) - x for x in range(len(data.names))], data.names)
    return fig

def get_empty_graph():
    #empty_graph
    empty_layout = go.Layout(plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    xaxis = dict(showticklabels=False, showgrid=False, zeroline = False),
    yaxis = dict(showticklabels = False, showgrid=False, zeroline = False),
    height=800, width=700)
    empty_graph = go.Figure()
    # empty_graph.update_layout(empty_layout)
    return empty_graph

def _build_tree_map(dataset):
    fig = px.treemap(dataset, path=[px.Constant("all"), 'lang', 'name'], values='count')
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    return fig

def get_data_composition_graph(selected_datasets=None, selected_points=None):
    if selected_points:
        filtered = data.filter_points(selected_datasets, selected_points)
        filtered = filtered.groupby(by=['name', 'lang']).count().reset_index()[['name', 'lang', 'id']]
        filtered.columns=['name', 'lang', 'count']
    else:
        filtered = data.composition[data.composition.name.isin(selected_datasets)]
    
    if filtered is None or not len(filtered):
        return get_empty_graph()
    return _build_tree_map(filtered)
    return fig