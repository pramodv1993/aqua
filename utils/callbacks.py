from dash import html, Input, Output, ctx, State, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from utils import plots
from utils import layout
from utils import data
prev_selected_datasets = []
prev_filtered = None
prev_s2_filtered = None
prev_s3_filtered = None


def define_callbacks(app):
    @app.callback(
    Output('dataset_selector', 'value'),
    Input('dimred', 'value'))
    def update_dataset(value):
        if value:
            data.change_dataset(value)
        plots.reset_graphs(stage_nums=[1,2,3,4])
        plots.prev_s1_g1 = plots.get_empty_graph()
        data.reset_metric_bounds()
        return (None, [])

    
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

    @app.callback(Output('stage1_g1', 'figure'),
               [Input('global_view', 'selectedData'),
                Input("refresh_view", "n_clicks")])
    def update_filtered_points(selectedData, n_clicks):
        global prev_selected_datasets, prev_filtered
        triggered_id = ctx.triggered_id
        if triggered_id=='refresh_view':
            prev_filtered = None
            plots.prev_s1_g1 = plots.get_empty_graph()
            return plots.prev_s1_g1
        if not selectedData or not len(selectedData['points']):
            return plots.prev_s1_g1
        #update graphs
        ids = [point['customdata'][0] for point in selectedData['points']]
        new_filtered = data.filter_points(ids=ids)
        prev_filtered = data.update_filtered_points(prev_filtered, new_filtered)
        plots.prev_s1_g1 = plots.get_scatter_plot(prev_filtered)
        return plots.prev_s1_g1

    @app.callback([Output('stage1_g2', 'figure'),
                Output('stage1_g3', 'figure'),
                Output('stage1_g3_selected_range', 'children'),
                Output('stage1_g4', 'figure'),
                Output('stage1_g4_selected_range', 'children'),
                Output('stage1_g5', 'figure'),
                Output('stage1_g5_selected_range', 'children'),
                Output('stage1_g6', 'figure'),
                Output('stage1_g6_selected_range', 'children'),
                Output('stage1_g7', 'figure'),
                Output('stage1_g7_selected_range', 'children'),
                Output('stage1_g8', 'figure'),
                Output('stage1_g8_selected_range', 'children'),
                Output('stage1_g9', 'figure'),
                Output('stage1_g9_selected_range', 'children')],
                
                [Input('global_view', 'selectedData'),
                Input('dataset_selector', "value"),
                Input("fixed_points", "n_clicks"),
                Input('refresh_view', 'n_clicks'),
                Input('stage1_g3_range', 'value'),
                Input('stage1_g4_range', 'value'),
                Input('stage1_g5_range', 'value'),
                Input('stage1_g6_range', 'value'),
                Input('stage1_g7_range', 'value'),
                Input('stage1_g8_range', 'value'),
                Input('stage1_g9_range', 'value'),
                ])
    def update_stage1(selected_points,\
        selected_datasets,\
        n_clicks,\
        refresh_n_clicks,\
        s1_g3_range=None,\
        s1_g4_range=None,\
        s1_g5_range=None,\
        s1_g6_range=None,\
        s1_g7_range=None,\
        s1_g8_range=None,\
        s1_g9_range=None,
        ):
        global prev_selected_datasets, prev_filtered, prev_s2_filtered, prev_s3_filtered
        triggered_id = ctx.triggered_id
        cnt_points = None
        filtered = None
        cnt_points_by_src = lambda df: df.groupby(by=['name', 'lang']).count().reset_index()[['name', 'lang', 'id']]
        s1_g3_selected_range = dbc.Label(f"Selected Range: {s1_g3_range}")
        s1_g4_selected_range = dbc.Label(f"Selected Range: {s1_g4_range}")
        s1_g5_selected_range = dbc.Label(f"Selected Range: {s1_g5_range}")
        s1_g6_selected_range = dbc.Label(f"Selected Range: {s1_g6_range}")
        s1_g7_selected_range = dbc.Label(f"Selected Range: {s1_g7_range}")
        s1_g8_selected_range = dbc.Label(f"Selected Range: {s1_g8_range}")
        s1_g9_selected_range = dbc.Label(f"Selected Range: {s1_g9_range}")

        if selected_datasets is not None:
            prev_selected_datasets = selected_datasets
        
        if triggered_id=="fixed_points":
            if prev_filtered is not None:
                cnt_points = cnt_points_by_src(prev_filtered)
                plots.update_dist_plots_for_stage(points=prev_filtered, stage_nums=[1,2])

        elif triggered_id=='global_view' and\
             selected_points and\
                 len(selected_points['points']):
                ids = [point['customdata'][0] for point in selected_points['points']]
                filtered = data.filter_points(prev_selected_datasets, ids)
                cnt_points = cnt_points_by_src(filtered)
                plots.update_dist_plots_for_stage(points=filtered, stage_nums=[1])
                
        elif triggered_id=="refresh_view":
            plots.reset_graphs(stage_nums=[1,2,3,4])
            prev_filtered = None
            prev_s2_filtered = None
            prev_s3_filtered = None
            data.reset_metric_bounds()
        #stage I
        elif triggered_id=="stage1_g3_range":
            lb, ub = s1_g3_range
            plots.prev_s1_g3 = plots.get_dist_plot(points=prev_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='total_words_per_doc')
        
        elif triggered_id=="stage1_g4_range":
            lb, ub = s1_g4_range
            plots.prev_s1_g4 = plots.get_dist_plot(points=prev_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='avg_word_length')
        
        elif triggered_id=="stage1_g5_range":
            lb, ub = s1_g5_range
            plots.prev_s1_g5 = plots.get_dist_plot(points=prev_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='total_num_sent')
        elif triggered_id=="stage1_g6_range":
            lb, ub = s1_g6_range
            plots.prev_s1_g6 = plots.get_dist_plot(points=prev_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='avg_sent_length')
        elif triggered_id=="stage1_g7_range":
            lb, ub = s1_g7_range
            plots.prev_s1_g7 = plots.get_dist_plot(points=prev_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='token_type_ratio')
        elif triggered_id=="stage1_g8_range":
            lb, ub = s1_g8_range
            plots.prev_s1_g8 = plots.get_dist_plot(points=prev_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='symbol_word_ratio')
        elif triggered_id=="stage1_g9_range":
            lb, ub = s1_g9_range
            plots.prev_s1_g9 = plots.get_dist_plot(points=prev_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='num_non_alphabet_words')
        elif triggered_id=='dataset_selector':
            #dataset_selector
            filtered = data.filter_points(prev_selected_datasets)
            if filtered is not None:
                cnt_points = cnt_points_by_src(filtered)
        
        if cnt_points is not None:
            cnt_points.columns=['name', 'lang', 'count']
            plots.prev_s1_g2 = plots.get_data_composition_graph(cnt_points)
        return (plots.prev_s1_g2,
                plots.prev_s1_g3, s1_g3_selected_range,
                plots.prev_s1_g4, s1_g4_selected_range,
                plots.prev_s1_g5, s1_g5_selected_range,
                plots.prev_s1_g6, s1_g6_selected_range,
                plots.prev_s1_g7, s1_g7_selected_range,
                plots.prev_s1_g8, s1_g8_selected_range,
                plots.prev_s1_g9, s1_g9_selected_range)
    

    @app.callback([Output('stage2_alert', 'displayed'),
                Output('stage2_g1', 'figure'),
                Output('stage2_g1_selected_range', 'children'),
                Output('stage2_g2', 'figure'),
                Output('stage2_g2_selected_range', 'children'),
                Output('stage2_g3', 'figure'),
                Output('stage2_g3_selected_range', 'children'),
                Output('stage2_g4', 'figure'),
                Output('stage2_g4_selected_range', 'children')],

                Input('stage2_trigger','n_clicks'),
                Input('stage2_g1_range', 'value'),
                Input('stage2_g2_range', 'value'),
                Input('stage2_g3_range', 'value'),
                Input('stage2_g4_range', 'value'),
                )
    def update_stage2(n_clicks,
        s2_g1_range=None,\
        s2_g2_range=None,\
        s2_g3_range=None,\
        s2_g4_range=None,):
        global prev_filtered, prev_s2_filtered
        is_alert_open = False
        triggered_id = ctx.triggered_id
        s2_g1_selected_range = dbc.Label(f"Selected Range: {s2_g1_range}")
        s2_g2_selected_range = dbc.Label(f"Selected Range: {s2_g2_range}")
        s2_g3_selected_range = dbc.Label(f"Selected Range: {s2_g3_range}")
        s2_g4_selected_range = dbc.Label(f"Selected Range: {s2_g4_range}")

        if triggered_id=="stage2_g1_range":
            lb, ub = s2_g1_range
            plots.prev_s2_g1 = plots.get_dist_plot(points=prev_s2_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='num_stopwords_per_doc')
        elif triggered_id=="stage2_g2_range":
            lb, ub = s2_g2_range
            plots.prev_s2_g2 = plots.get_dist_plot(points=prev_s2_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='num_abbreviations_per_doc')
        elif triggered_id=="stage2_g3_range":
            lb, ub = s2_g3_range
            plots.prev_s2_g3 = plots.get_dist_plot(points=prev_s2_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='num_exact_duplicates')
        elif triggered_id=="stage2_g4_range":
            lb, ub = s2_g4_range
            plots.prev_s2_g4 = plots.get_dist_plot(points=prev_s2_filtered,
                                             lb=lb,
                                             ub=ub,
                                             metric='num_near_duplicates')
        elif n_clicks and prev_filtered is not None:
            #stage2_trigger
            print("before filter from s1", prev_filtered.shape)
            new_filtered = data.apply_metric_filters(
                data.get_metrics_for_points(prev_filtered.id))
            prev_s2_filtered = new_filtered
            print("after filter from s1", new_filtered.shape)
            plots.update_dist_plots_for_stage(points=prev_s2_filtered, stage_nums=[2])
            is_alert_open = True
        return (is_alert_open,
                plots.prev_s2_g1, s2_g1_selected_range,
                plots.prev_s2_g2, s2_g2_selected_range,
                plots.prev_s2_g3, s2_g3_selected_range,
                plots.prev_s2_g4, s2_g4_selected_range)
    
    @app.callback([
                Output('stage3_alert', 'displayed'),
                Output('stage3_g1', 'figure'),
                Output('stage3_g2', 'figure')],
                [Input('stage3_trigger','n_clicks')])
    def update_stage3(n_clicks):
        global prev_s2_filtered, prev_s3_filtered
        is_alert_open = False
        if n_clicks and prev_s2_filtered is not None:
            is_alert_open=True
            print("before filter from s2", prev_s2_filtered.shape)
            prev_s3_filtered = data.filter_points(
               ids=data.apply_metric_filters(prev_s2_filtered).id.tolist())
            print("after filter from s2", prev_s3_filtered.shape)
            plots.update_classifier_plot(points=prev_s3_filtered)
            plots.update_topics_plot(points=prev_s3_filtered)
        return (is_alert_open,
                plots.prev_s3_g1,
                plots.prev_s3_g2)

    @app.callback([
                Output('stage4_alert', 'displayed'),
                Output('stage4_g1', 'figure'),
                Output('stage4_g2', 'figure')],
                [Input('stage4_trigger','n_clicks')])
    def update_stage4(n_clicks):
        global prev_s3_filtered
        is_alert_open = False
        if n_clicks and prev_s3_filtered is not None:
            is_alert_open=True
        plots.update_bias_plot(points=prev_s3_filtered)
        plots.update_toxicity_plot(points=prev_s3_filtered)
        return (is_alert_open,
            plots.prev_s4_g1,
            plots.prev_s4_g2)
    
    @app.callback(
        Output("words_in_topic", "figure"),
        Input('stage3_g2', 'clickData'),
    )
    def update_words_in_topic(clickData):
        figs = plots.get_empty_graph()
        if clickData is not None:
            return plots.update_topic_words_plot(clickData)
        return figs

    @app.callback([Output('export_dataset_download', 'data'),
                   Output('export_dialog', 'displayed'),
                   Output('export_dialog', 'message')],
    [   
        Input('export_dataset_s1', 'n_clicks'),
        Input('export_dataset_s2', 'n_clicks'),
        Input('export_dataset_s3', 'n_clicks'),
        Input('export_dataset_s4', 'n_clicks')],
    prevent_initial_call=True)
    def export_dataset(s1_click, s2_click, s3_click, s4_click):
        global prev_filtered, prev_s2_filtered, prev_s3_filtered
        triggered_id = ctx.triggered_id
        if triggered_id=='export_dataset_s1':
            snapshot = prev_filtered
        else:
            snapshot = prev_s2_filtered
        op = "stage{}.csv".format(triggered_id[-1])
        return (dcc.send_data_frame(snapshot.to_csv, op),
                True,
                'Exporting as file: {}?'.format(op)
        )
    
# switch to next tab once the button is pressed
    @app.callback(Output('tabs', 'active_tab'),
        [Input('stage2_trigger', 'n_clicks'),
            Input('stage3_trigger', 'n_clicks'),
            Input('stage4_trigger', 'n_clicks')])
    def switch_tab(n_click1, n_click2, n_click3):
        triggered_id = ctx.triggered_id
        if triggered_id=='stage2_trigger':
            return 'stage2_tab'
        elif triggered_id=='stage3_trigger':
            return 'stage3_tab'
        elif triggered_id=='stage4_trigger':
            return 'stage4_tab'
        else:
            return 'stage1_tab'

#pipeline image button
#     @app.callback(
#     Output("my_modal", "is_open"),
#     [Input("pipeline", "n_clicks"), Input("close_modal", "n_clicks")],
#     [State("my_modal", "is_open")],
# )
#     def toggle_modal(n1, n2, is_open):
#         if n1 or n2:
#             return not is_open
#         return is_open