import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from facebook_data_analysis import common
from facebook_data_analysis.conversation_analysis import message_handling
from facebook_data_analysis.global_vars import messages_cols
from facebook_data_analysis.tools import helpers


def base_elem():
    return dcc.Tab(
        label="Start Here",
        id="home-tab",
        children=[
            # Data file
            html.Label(
                "Anonymize data ? (this will replace all names by fake ones. "
                "Meant for demo purposes; may take a very long time at the first run)"
            ),
            dcc.RadioItems(
                id="anonymize",
                options=[{"label": "Yes", "value": 1}, {"label": "No", "value": 0}],
                value=0,
            ),
            html.Label("Path to you facebook data folder"),
            dcc.Input(
                id="facebook-data-folder",
                type="text",
                debounce=True,
                placeholder="/home/me/downloads/facebook-myname",
                size="100",
            ),
            html.P(id="status-choose-path"),
            html.P(id="op-compute-data", style={"display": "none"}, children=""),
            html.P(id="status-compute_data"),
            # My name input
            html.Label("Your facebook name"),
            dcc.Dropdown(
                id="facebook-name",
                options=[],
                disabled=True,
                placeholder="Upload your data first",
                value="",
            ),
            # Updating this component's children causes all of the other tabs to activate
            html.P(id="aggregation-finished"),
        ],
    )


def _attach_get_data_folder(app: dash.Dash):
    @app.callback(
        [
            Output("op-compute-data", "children"),
            Output("status-choose-path", "children"),
            Output("status-choose-path", "style"),
            Output("facebook-data-folder", "disabled"),
        ],
        [Input("facebook-data-folder", "value")],
    )  # pylint: disable=unused-variable
    def get_data_folder(input_string):
        if not input_string:
            return "", dash.no_update, dash.no_update, False
        if not os.path.isdir(input_string):
            return "", "This path is not a folder!", {"color": "red"}, False
        return input_string, "Successfully received path. Processing data...", {}, True


def _attach_process_data(app: dash.Dash):
    @app.callback(
        [
            Output("status-compute_data", "children"),
            Output("status-compute_data", "style"),
            Output("facebook-name", "disabled"),
            Output("facebook-name", "placeholder"),
        ],
        [Input("op-compute-data", "children")],
        [State("anonymize", "value")],
    )  # pylint: disable=unused-variable
    def process_data(data_path, anonymize):
        if not data_path:
            return dash.no_update, dash.no_update, True, dash.no_update
        try:
            conversations = message_handling.get_conversations(data_path)
            messages = message_handling.generate_messages_dataframe(conversations)

            if anonymize:
                messages = helpers.anonymize_data(messages)

            common.conversations_df = messages
            return (
                f"Successfully recovered {common.conversations_df.shape[0]} messages. Now proceed to selecting "
                f"your facebook user name.",
                {},
                False,
                "John Doe",
            )
        except Exception as e:  # pylint: disable=broad-except
            return (
                "An error occurred while processing the data ! Please check the logs, refresh and try again",
                {"color": "red"},
                dash.no_update,
                dash.no_update,
            )


def _attach_prepare_dropdown(app: dash.Dash):
    """When the data has been loaded and the name selection enabled,
        update the options to select your own name"""

    @app.callback(
        [Output("facebook-name", "options")], [Input("facebook-name", "disabled")]
    )  # pylint: disable=unused-variable
    def prepare_dropdown(disabled: bool):
        if disabled:
            return dash.no_update

        friends_list = (
            common.conversations_df[messages_cols.sender]
            .sort_values()
            .unique()
            .tolist()
        )
        return (
            [{"label": friend, "value": friend} for friend in friends_list if friend],
        )


def _attach_save_my_name(app: dash.Dash):
    """Once the name has been selected, compute the conversation aggregations"""

    @app.callback(
        [Output("aggregation-finished", "children")], [Input("facebook-name", "value")]
    )  # pylint: disable=unused-variable
    def save_my_name(my_facebook_name):
        if not my_facebook_name:
            return (dash.no_update,)
        common.my_name = common.FacebookName(my_facebook_name)
        return ("Ready to proceed!",)


def attach(app):
    _attach_get_data_folder(app)
    _attach_process_data(app)
    _attach_prepare_dropdown(app)
    _attach_save_my_name(app)
    return base_elem()
