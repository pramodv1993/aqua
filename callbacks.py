from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL, ctx
import plots
from utils import data
prev_selected_datasets = []
prev_filtered = None
prev_s1_g1 = plots.get_empty_graph()

def define_callbacks(app):
    @app.callback(
        [Output('global_view', 'figure'),
        Output('stage1_g4', 'figure'),
        Output('stage2_g1', 'figure'),
        Output('stage3_g1', 'figure')
        ],
        [Input('dataset_selector', "value")]
    )
    def select_datasets(selected_datasets):
        global prev_selected_datasets
        prev_selected_datasets = selected_datasets
        global_view, _ = plots.get_or_update_scatter_plot(selected_datasets)
        s1_g4 = plots.get_empty_graph()
        s2_g1 = plots.get_empty_graph()
        s3_g1 = plots.get_empty_graph()
        return (global_view, s1_g4, s2_g1, s3_g1) 

    @app.callback([Output('stage1_g1', 'figure'),
                Output('stage1_g3', 'figure')],
               [Input('global_view', 'selectedData'),
                Input("refresh_view", "n_clicks")])
    def update_data_selection_graph(selectedData, n_clicks):
        global prev_selected_datasets, prev_filtered, prev_s1_g1
        triggered_id = ctx.triggered_id
        if triggered_id=='refresh_view':
            prev_filtered = None
            prev_s1_g1 = plots.get_empty_graph()
            return (prev_s1_g1, plots.get_empty_graph())
        if not selectedData or not len(selectedData['points']):
            return prev_s1_g1,\
                plots.get_empty_graph()
        ids = [point['customdata'][0] for point in selectedData['points']]
        prev_s1_g1, prev_filtered = plots.get_or_update_scatter_plot(ids=ids,\
             datasets=prev_selected_datasets, prev_filtered=prev_filtered)
        s1_g3 = plots.get_dist_plot(ids)
        return (prev_s1_g1, s1_g3)

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