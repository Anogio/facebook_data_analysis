import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
from facebook_data_analysis import common
from facebook_data_analysis.global_vars import messages_cols


def friend_stats(friend_name: str):
    from_friend_in_group_chat = common.conversations_df.loc[
        (common.conversations_df[messages_cols.sender] == friend_name)
        & (common.conversations_df[messages_cols.conv_type] != "Regular")
    ].shape[0]

    in_dm = common.conversations_df.loc[
        common.conversations_df[messages_cols.conversation] == friend_name
    ]
    from_me_in_dm = in_dm.loc[in_dm[messages_cols.sender] != friend_name].shape[0]
    from_friend_in_dm = in_dm.loc[in_dm[messages_cols.sender] == friend_name].shape[0]

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=from_me_in_dm,
            title={"text": "DMs you sent to them"},
            domain={"row": 0, "column": 0},
        )
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=from_friend_in_dm,
            title={"text": "DMs they sent to you"},
            domain={"row": 0, "column": 1},
        )
    )

    fig.add_trace(
        go.Indicator(
            mode="number",
            value=from_friend_in_group_chat,
            title={"text": "Messages sent by them to group chats"},
            domain={"row": 0, "column": 2},
        )
    )

    fig.update_layout(grid={"rows": 1, "columns": 3, "pattern": "independent"})
    return dcc.Graph(figure=fig)


def friend_conversations_breakdown(friend_name: str) -> dcc.Graph:
    friend_df = common.conversations_df.loc[
        common.conversations_df[messages_cols.sender] == friend_name
    ].replace({messages_cols.conversation: {friend_name: "Private message"}})
    return dcc.Graph(
        figure=px.pie(
            friend_df,
            names=messages_cols.conversation,
            title="Number of messages received from this friend, by conversation",
        )
    )


graphs = [friend_stats, friend_conversations_breakdown]
