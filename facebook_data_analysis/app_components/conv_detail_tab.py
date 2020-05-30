from typing import Dict
from typing import List
from typing import Tuple

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from facebook_data_analysis import common
from facebook_data_analysis.global_vars import messages_cols


def base_elem():
    return dcc.Tab(
        id="conversation-tab",
        label="Detailed conversation view",
        disabled=True,
        children=[
            html.Label("Select conversation for detailed view"),
            dcc.Dropdown(id="conversation-detail-name", options=[], value=""),
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
    def update_friends(friend_tab_disabled: bool) -> List[Dict[str, str]]:
        if friend_tab_disabled:
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


def attach(app: dash.Dash):
    _attach_activate_tab(app)
    _attach_update_conversations(app)
    return base_elem()
