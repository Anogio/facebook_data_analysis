from typing import Dict
from typing import List
from typing import Tuple

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from facebook_data_analysis import common
from facebook_data_analysis.app_components.conv_detail_tab.graphs import graphs
from facebook_data_analysis.global_vars import messages_cols


def base_elem():
    return dcc.Tab(
        id="conversation-tab",
        label="Detailed conversation view",
        disabled=True,
        children=[
            html.Label("Select conversation for detailed view"),
            dcc.Dropdown(id="conversation-detail-name", options=[], value=""),
            html.Div(
                id="conversation-graphs",
                style={"display": "none"},
                children=[dcc.Graph()],
            ),
        ],
    )


def _attach_activate_tab(app: dash.Dash):
    @app.callback(
        [Output("conversation-tab", "disabled")],
        [Input("aggregation-finished", "children")],
    )  # pylint: disable=unused-variable
    def activate_tab(agg_finished_text: str) -> Tuple[bool]:
        if not agg_finished_text:
            return (dash.no_update,)
        return (False,)


def _attach_update_conversations(app: dash.Dash):
    @app.callback(
        Output("conversation-detail-name", "options"),
        [Input("conversation-tab", "disabled")],
    )  # pylint: disable=unused-variable
    def update_conversations(conv_tab_disabled: bool) -> List[Dict[str, str]]:
        if conv_tab_disabled:
            return dash.no_update

        group_conversations = (
            common.conversations_df.loc[
                common.conversations_df[messages_cols.conv_type] != "Regular"
            ][[messages_cols.conversation, messages_cols.conv_id]]
            .drop_duplicates()
            .values.tolist()
        )
        group_conversations = sorted(map(tuple, group_conversations))

        return [
            {"label": conv_name, "value": conv_id}
            for conv_name, conv_id in group_conversations
        ]


def compute_graphs(conv_name: str) -> List[dcc.Graph]:
    return [graph(conv_name) for graph in graphs]


def _attach_compute_and_show_graphs(app: dash.Dash):
    @app.callback(
        [
            Output("conversation-graphs", "style"),
            Output("conversation-graphs", "children"),
        ],
        [Input("conversation-detail-name", "value")],
    )  # pylint: disable=unused-variable
    def compute_and_show_graphs(conv_name: str):
        if not conv_name:
            return {"display": "none"}, []
        return {}, compute_graphs(conv_name)


def attach(app: dash.Dash):
    _attach_activate_tab(app)
    _attach_update_conversations(app)
    _attach_compute_and_show_graphs(app)
    return base_elem()
