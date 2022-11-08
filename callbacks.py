from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import plots

def define_callbacks(app):
    @app.callback(
        Output('global_view', 'figure'),
        [Input('dataset_selector', "value")]
    )
    def select_datasets(selected_datasets):
        return plots.get_scatter_plot(selected_datasets)