from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import plots

def define_callbacks(app):
    @app.callback(
        [Output('global_view', 'figure'),
        Output('stagei_g1', 'figure'),
        Output('stagei_g2', 'figure'),
        Output('stagei_g3', 'figure'),
        Output('stageii_g1', 'figure'),
        Output('stageiii_g1', 'figure')
        ],
        [Input('dataset_selector', "value")]
    )
    def select_datasets(selected_datasets):
        global_view = plots.get_scatter_plot(selected_datasets)
        s1_g1,s1_g2,s1_g3 = plots.get_empty_graph(),\
            plots.get_empty_graph(),\
            plots.get_empty_graph()
        s2_g1 = plots.get_bar_graph(selected_datasets)
        s3_g1 = plots.get_dist_plot(selected_datasets)
        return (global_view, s1_g1, s1_g2, s1_g3,\
            s2_g1, s3_g1) 