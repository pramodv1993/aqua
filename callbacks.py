from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL, ctx
import plots
from utils import data
prev_selected_datasets = []
prev_filtered = None
prev_s1_g1 = plots.get_empty_graph()
prev_s1_g3 = plots.get_empty_graph()
prev_s1_g2 = plots.get_empty_graph()

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
                Output('stage1_g4', 'figure')],
               [Input('global_view', 'selectedData'),
                Input("refresh_view", "n_clicks")])
    def update_filtered_points(selectedData, n_clicks):
        global prev_selected_datasets, prev_filtered, prev_s1_g1
        triggered_id = ctx.triggered_id
        if triggered_id=='refresh_view':
            prev_filtered = None
            return tuple([plots.get_empty_graph()] * 2)
        if not selectedData or not len(selectedData['points']):
            return tuple([prev_s1_g1, plots.get_empty_graph()])
        #update graphs
        ids = [point['customdata'][0] for point in selectedData['points']]
        new_filtered = data.filter_points(ids=ids)
        prev_filtered = data.update_filtered_points(prev_filtered, new_filtered)
        prev_s1_g1 = plots.get_scatter_plot(prev_filtered)
        return tuple([prev_s1_g1, plots.get_empty_graph()])

    @app.callback([Output('stage1_g2', 'figure'),
                Output('stage1_g3', 'figure'),
                Output('stage1_g3_selected_range', 'children')],
                [Input('global_view', 'selectedData'),
                Input('dataset_selector', "value"),
                Input("fixed_points", "n_clicks"),
                Input('refresh_view', 'n_clicks'),
                Input('stage1_g3_range', 'value')])
    def update_graphs(selected_points, selected_datasets, n_clicks, refresh_n_clicks,\
        s1_g3_range=None):
        global prev_selected_datasets, prev_filtered, prev_s1_g3, prev_s1_g2
        triggered_id = ctx.triggered_id
        cnt_points = None
        filtered = None
        cnt_points_by_src = lambda df: df.groupby(by=['name', 'lang']).count().reset_index()[['name', 'lang', 'id']]
        s1_g3_selected_range = html.H4(f"Selected Range: {s1_g3_range}")

        if selected_datasets is not None:
            prev_selected_datasets = selected_datasets
        
        if triggered_id=="fixed_points":
            if prev_filtered is not None:
                cnt_points = cnt_points_by_src(prev_filtered)
                prev_s1_g3 = plots.get_dist_plot(points=prev_filtered)

        elif triggered_id=='global_view' and\
             selected_points and\
                 len(selected_points['points']):
                ids = [point['customdata'][0] for point in selected_points['points']]
                filtered = data.filter_points(prev_selected_datasets, ids)
                cnt_points = cnt_points_by_src(filtered)
                prev_s1_g3 = plots.get_dist_plot(points=filtered)
        
        elif triggered_id=="refresh_view":
            prev_s1_g2 = plots.get_empty_graph()
            prev_s1_g3 = plots.get_empty_graph()
        
        elif triggered_id=="stage1_g3_range":
            lb, ub = s1_g3_range
            prev_s1_g3 = plots.get_dist_plot(points=prev_filtered, lb=lb, ub=ub)
        else:
            #dataset_selector
            filtered = data.filter_points(prev_selected_datasets)
            if filtered is not None:
                cnt_points = cnt_points_by_src(filtered)
        
        if cnt_points is not None:
            cnt_points.columns=['name', 'lang', 'count']
            prev_s1_g2 = plots.get_data_composition_graph(cnt_points)
        return (prev_s1_g2, prev_s1_g3, s1_g3_selected_range)