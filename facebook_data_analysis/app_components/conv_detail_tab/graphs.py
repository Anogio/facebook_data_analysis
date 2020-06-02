import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
from facebook_data_analysis import common
from facebook_data_analysis.global_vars import messages_cols


def conversation_stats(conv_id: str):
    conv_df = common.conversations_df.loc[
        common.conversations_df[messages_cols.conv_id] == conv_id
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="number", value=conv_df.shape[0], title="Number of exchanged messages"
        )
    )
    return dcc.Graph(figure=fig)


def conversation_activity_by_friend(conv_id: str) -> dcc.Graph:
    conv_df = common.conversations_df.loc[
        common.conversations_df[messages_cols.conv_id] == conv_id
    ]
    return dcc.Graph(
        figure=px.pie(
            conv_df,
            names=messages_cols.sender,
            title="Number of messages sent by this friend to the conversation",
        )
    )


graphs = [conversation_stats, conversation_activity_by_friend]
