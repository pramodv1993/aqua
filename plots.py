import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import numpy as np

def get_scatter_plot():
    points = pd.DataFrame(np.random.randint(0, 100, size=(100,2)), columns=list('AB'))
    fig = px.scatter(points, x='A', y='B')
    fig.update_layout(title='datasets')
    return dcc.Graph(figure=fig)

def get_bar_graph():
    fig =  px.bar(x=[1,2], y = [3,4])
    fig.update_layout(title="Metrics")
    return dcc.Graph(figure=fig)
