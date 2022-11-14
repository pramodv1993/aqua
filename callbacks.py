from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL, ctx
import plots
from utils import data
prev_selected_datasets = []
prev_filtered = None
prev_s1_g1 = plots.get_empty_graph()

def define_callbacks(app):
    @app.callback(
        Output('global_view', 'figure'),
        [Input('dataset_selector', "value")]
    )
    def select_datasets(selected_datasets):
        global prev_selected_datasets
        prev_selected_datasets = selected_datasets
        filtered_points = data.filter_points(selected_datasets=prev_selected_datasets)
        global_view = plots.get_scatter_plot(filtered_points)
        return global_view

    @app.callback([Output('stage1_g1', 'figure'),
                Output('stage1_g3', 'figure'),
                Output('stage1_g4', 'figure')],
               [Input('global_view', 'selectedData'),
                Input("refresh_view", "n_clicks")])
    def update_graphs(selectedData, n_clicks):
        global prev_selected_datasets, prev_filtered, prev_s1_g1
        triggered_id = ctx.triggered_id
        if triggered_id=='refresh_view':
            prev_filtered = None
            return tuple([plots.get_empty_graph()] * 3)
        if not selectedData or not len(selectedData['points']):
            #retain the previously filtered points
            return tuple([prev_s1_g1] + [plots.get_empty_graph()] * 2)
        #update graphs
        ids = [point['customdata'][0] for point in selectedData['points']]
        new_filtered = data.filter_points(ids=ids)
        prev_filtered = data.update_filtered_points(prev_filtered, new_filtered)
        prev_s1_g1 = plots.get_scatter_plot(prev_filtered)
        s1_g3 = plots.get_dist_plot(ids)
        return tuple([prev_s1_g1, s1_g3] + [plots.get_empty_graph()] * 1)

    @app.callback(Output('stage1_g2', 'figure'),
                [Input('global_view', 'selectedData'),
                Input('dataset_selector', "value"),
                Input("fixed_points", "n_clicks"),
                Input('refresh_view', 'n_clicks')])
    def update_data_composition(selected_points, selected_datasets, n_clicks, refresh_n_clicks):
        global prev_selected_datasets, prev_filtered
        prev_selected_datasets = selected_datasets
        triggered_id = ctx.triggered_id
        if triggered_id=="fixed_points":
            return plots.get_data_composition_graph(selected_points=prev_filtered.id.tolist())
        if triggered_id=='dataset_selector' or triggered_id=='refresh_view' or not selected_points:
            return plots.get_data_composition_graph(prev_selected_datasets, selected_points=None)
        ids = [point['customdata'][0] for point in selected_points['points']]
        return plots.get_data_composition_graph(prev_selected_datasets, selected_points=ids)