import dash_core_components as dcc
import plotly.express as px
from facebook_data_analysis import common
from facebook_data_analysis.global_vars import messages_cols


def top_friends_dm() -> dcc.Graph:
    friends_dm = common.conversations_df.loc[
        common.conversations_df[messages_cols.conv_type] == "Regular"
    ]
    friend_dm_count = (
        friends_dm.groupby(
            [messages_cols.conv_id, messages_cols.conversation, messages_cols.sender]
        )
        .size()
        .reset_index(name="n_direct_messages")
    )

    friend_dm_count.loc[
        friend_dm_count[messages_cols.sender] != common.my_name.name, "Sent by"
    ] = "Them"
    friend_dm_count.loc[
        friend_dm_count[messages_cols.sender] == common.my_name.name, "Sent by"
    ] = "Me"
    friend_dm_count["Friend"] = friend_dm_count[messages_cols.conversation]

    friends_count_total = (
        friend_dm_count.groupby(messages_cols.conv_id)["n_direct_messages"]
        .sum()
        .sort_values()
    )
    selected_friends = friends_count_total.iloc[-25:]
    friends_dm_count_top = friend_dm_count.loc[
        friend_dm_count[messages_cols.conv_id].isin(selected_friends.index)
    ]
    fig = px.bar(
        friends_dm_count_top,
        y="Friend",
        x="n_direct_messages",
        orientation="h",
        color="Sent by",
        hover_data=["Sent by", "Friend"],
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        title="Top friends by exchanged messages",
        xaxis_title="Direct messages",
        width=1200,
        height=500,
    )

    return dcc.Graph(figure=fig)


def top_group_conversations():
    group_conversations = common.conversations_df.loc[
        common.conversations_df[messages_cols.conv_type] != "Regular"
    ]
    group_conversations.loc[
        group_conversations[messages_cols.sender] != common.my_name.name, "Sent by"
    ] = "Others"
    group_conversations.loc[
        group_conversations[messages_cols.sender] == common.my_name.name, "Sent by"
    ] = "Me"

    group_conversations_count = (
        group_conversations.groupby(
            [messages_cols.conv_id, messages_cols.conversation, "Sent by"]
        )
        .size()
        .reset_index(name="n_group_messages")
    )

    conversations_count_total = (
        group_conversations_count.groupby([messages_cols.conv_id])["n_group_messages"]
        .sum()
        .sort_values()
    )
    selected_conversations = conversations_count_total.iloc[-25:]

    conversations_count_top = group_conversations_count.loc[
        group_conversations_count[messages_cols.conv_id].isin(
            selected_conversations.index
        )
    ]

    fig = px.bar(
        conversations_count_top,
        y=messages_cols.conversation,
        x="n_group_messages",
        orientation="h",
        color="Sent by",
        hover_data=["Sent by", messages_cols.conversation],
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        title="Top conversations by exchanged messages",
        xaxis_title="Messages",
        yaxis_title="Conversation",
        width=1200,
        height=500,
    )

    return dcc.Graph(figure=fig)


graphs = [top_friends_dm, top_group_conversations]
