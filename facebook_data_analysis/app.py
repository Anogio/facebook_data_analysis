from typing import List
from typing import Tuple

import dash
import dash_core_components as dcc
import dash_html_components as html
from facebook_data_analysis.app_components import friend_detail_tab
from facebook_data_analysis.app_components import home_tab

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
                dcc.Tabs(
                    children=[
                        home_tab.attach(app),
                        # Friend name input
                        friend_detail_tab.attach(app),
                        # Conversation name input
                        dcc.Tab(
                            label="Detailed conversation view",
                            children=[
                                html.Label("Select conversation for detailed view"),
                                dcc.Dropdown(
                                    options=[
                                        {"label": conv_name, "value": conv_id}
                                        for conv_id, conv_name in self.group_conversations_list()
                                    ]
                                ),
                            ],
                        ),
                    ]
                ),
            ]
        )
        return app

    @staticmethod
    def group_conversations_list() -> List[Tuple[str, str]]:
        # conversations = (
        #     self.conversations_df.loc[
        #         self.conversations_df[messages_cols.conv_type] != "Regular"
        #     ][[messages_cols.conv_id, messages_cols.conversation]]
        #     .drop_duplicates()
        #     .values.tolist()
        # )
        # return sorted(map(tuple, conversations))  # type: ignore
        return []


if __name__ == "__main__":
    dash_app = AppMaker(None, None)()
    print("UP")
    dash_app.run_server(debug=False)
