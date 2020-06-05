from typing import List

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from facebook_data_analysis.app_components.overview_tab.graphs import graphs


def base_elem():
    return dcc.Tab(
        id="overview-tab",
        label="General overview",
        disabled=True,
        children=[
            html.Div(
                id="overview-graphs", style={"display": "none"}, children=[dcc.Graph()]
            )
        ],
    )


def _attach_activate_tab(app: dash.Dash):
    @app.callback(
        [Output("overview-tab", "disabled")],
        [Input("aggregation-finished", "children")],
    )  # pylint: disable=unused-variable
    def activate_tab(agg_finished_text):
        if not agg_finished_text:
            return (dash.no_update,)
        return (False,)


def compute_graphs() -> List[dcc.Graph]:
    return [graph() for graph in graphs]


def _attach_compute_and_show_graphs(app: dash.Dash):
    @app.callback(
        [Output("overview-graphs", "style"), Output("overview-graphs", "children")],
        [Input("overview-tab", "disabled")],
    )  # pylint: disable=unused-variable
    def compute_and_show_graphs(disabled):
        if disabled:
            return {"display": "none"}, []
        return {}, compute_graphs()


def attach(app: dash.Dash):
    _attach_activate_tab(app)
    _attach_compute_and_show_graphs(app)
    return base_elem()
