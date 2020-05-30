from typing import List

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from facebook_data_analysis import common
from facebook_data_analysis.app_components.friend_detail_tab.graphs import graphs
from facebook_data_analysis.global_vars import messages_cols


def base_elem():
    return dcc.Tab(
        id="friend-tab",
        label="Detailed friend view",
        disabled=True,
        children=[
            html.Label("Select friend for detailed view"),
            dcc.Dropdown(id="friend-detail-name", options=[], value=""),
            html.Div(
                id="friend-graphs", style={"display": "none"}, children=[dcc.Graph()]
            ),
        ],
    )


def _attach_activate_tab(app: dash.Dash):
    @app.callback(
        [Output("friend-tab", "disabled")], [Input("aggregation-finished", "children")]
    )  # pylint: disable=unused-variable
    def activate_tab(agg_finished_text):
        if not agg_finished_text:
            return (dash.no_update,)
        return (False,)


def _attach_update_friends(app: dash.Dash):
    @app.callback(
        [Output("friend-detail-name", "options")], [Input("friend-tab", "disabled")]
    )  # pylint: disable=unused-variable
    def update_friends(friend_tab_disabled):
        if friend_tab_disabled:
            return (dash.no_update,)

        friends_list = (
            common.conversations_df[messages_cols.sender]
            .sort_values()
            .unique()
            .tolist()
        )
        return (
            [{"label": friend, "value": friend} for friend in friends_list if friend],
        )


def compute_graphs(friend_name: str) -> List[dcc.Graph]:
    return [graph(friend_name) for graph in graphs]


def _attach_compute_and_show_graphs(app: dash.Dash):
    @app.callback(
        [Output("friend-graphs", "style"), Output("friend-graphs", "children")],
        [Input("friend-detail-name", "value")],
    )  # pylint: disable=unused-variable
    def compute_and_show_graphs(friend_name: str):
        if not friend_name:
            return {"display": "none"}, []
        return {}, compute_graphs(friend_name)


def attach(app: dash.Dash):
    _attach_activate_tab(app)
    _attach_update_friends(app)
    _attach_compute_and_show_graphs(app)
    return base_elem()
