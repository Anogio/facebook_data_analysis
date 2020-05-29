from typing import List
from typing import Tuple

import dash
import dash_core_components as dcc
import dash_html_components as html
from facebook_data_analysis.conversation_analysis import message_handling
from facebook_data_analysis.global_vars import messages_cols

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


class AppMaker:
    def __init__(self, conversations_df, conversations_agg_df):
        self.conversations_df = conversations_df
        self.conversations_agg_df = conversations_agg_df

    def __call__(self):
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

        app.layout = html.Div(
            children=[
                html.H1(children="Facebook Data Analysis"),
                # Data file
                html.Label("You facebook data (as a .zip file)"),
                dcc.Upload(
                    id="facebook-data",
                    children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                    multiple=False,
                ),
                # My name input
                html.Label("Your facebook name"),
                dcc.Dropdown(
                    options=[
                        {"label": friend, "value": friend}
                        for friend in self.friends_list()
                        if friend
                    ]
                ),
                # Friend name input
                html.Label("Select friend for detailed view"),
                dcc.Dropdown(
                    options=[
                        {"label": friend, "value": friend}
                        for friend in self.friends_list()
                        if friend
                    ]
                ),
                # Conversation name input
                html.Label("Select conversation for detailed view"),
                dcc.Dropdown(
                    options=[
                        {"label": conv_name, "value": conv_id}
                        for conv_id, conv_name in self.group_conversations_list()
                    ]
                ),
            ]
        )
        return app

    def friends_list(self) -> List[str]:
        return (
            self.conversations_df[messages_cols.sender].sort_values().unique().tolist()
        )

    def group_conversations_list(self) -> List[Tuple[str, str]]:
        conversations = (
            self.conversations_df.loc[
                self.conversations_df[messages_cols.conv_type] != "Regular"
            ][[messages_cols.conv_id, messages_cols.conversation]]
            .drop_duplicates()
            .values.tolist()
        )
        return sorted(map(tuple, conversations))  # type: ignore


if __name__ == "__main__":
    data_folder = "/home/anog/Downloads/facebook-antoineogier"
    MY_NAME = "Antoine Ogier"
    messages_df, conversation_stat_df = message_handling.get_messages_with_post_treatment(
        MY_NAME, data_folder
    )

    dash_app = AppMaker(messages_df, conversation_stat_df)()
    print("UP")
    dash_app.run_server(debug=True)
