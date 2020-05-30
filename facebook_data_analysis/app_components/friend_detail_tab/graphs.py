import dash_core_components as dcc
import plotly.express as px
from facebook_data_analysis import common
from facebook_data_analysis.global_vars import messages_cols


def friend_conversations_breakdown(friend_name: str) -> dcc.Graph:
    friend_df = common.conversations_df[
        common.conversations_df[messages_cols.sender] == friend_name
    ].replace({messages_cols.conversation: {friend_name: "Private message"}})
    return dcc.Graph(
        figure=px.pie(
            friend_df,
            names=messages_cols.conversation,
            title="Number of messages received from this friend, by conversation",
        )
    )


graphs = [friend_conversations_breakdown]
