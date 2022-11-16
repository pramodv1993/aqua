from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

from utils import data

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

def reset_graphs(stage_num=None):
    if stage_num:
        for graph_num in range(1, data.num_graphs[f'stage{stage_num}']+1):
            globals()[f'prev_s{stage_num}_g{graph_num}'] = get_empty_graph()

def update_dist_plots_for_stage(points, stage_num=None, ub=None, lb=None):
    if stage_num:
        for graph_num, metric in data.stage_vs_metrics[f'stage{stage_num}']:
            globals()[f'prev_s{stage_num}_g{graph_num}'] = get_dist_plot(points, lb, ub, metric)


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

def get_dist_plot(points, lb=None, ub=None, metric=None):
    if points is None:
        return get_empty_graph()
    metrics_for_points = data.get_metrics_for_points(points.id)
    fig = px.histogram(metrics_for_points, x=metric, marginal='box', color='name')
    if lb:
        fig.add_vline(x=lb, line_width=2, line_dash='dash')
    if ub:
        fig.add_vline(x=ub, line_width=2, line_dash='dash')
    return fig

def _build_tree_map(dataset):
    fig = px.treemap(dataset, path=[px.Constant("all"), 'lang', 'name'], values='count')
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    return fig

def get_data_composition_graph(points=None):
    if points is None:
        return get_empty_graph()
    return _build_tree_map(points)