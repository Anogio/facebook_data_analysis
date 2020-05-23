import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from facebook_data_analysis.conversation_analysis.activity_graphs import save_graph
from facebook_data_analysis.global_vars import messages_cols
from facebook_data_analysis.tools.helpers import cached
from sklearn.manifold import MDS
from tqdm import tqdm


@cached("people_distance.db")
def get_people_distances(messages_df, conversations_df, min_messages_to_appear=10):
    group_conversations = conversations_df.loc[conversations_df["n_participants"] > 2][
        "conversation_name"
    ]

    messages_in_group_conversations = messages_df[
        messages_df[messages_cols.conversation].isin(group_conversations.values)
    ]
    friends_in_group_conversations = messages_in_group_conversations.groupby(
        messages_cols.sender
    )[messages_cols.timestamp].count()
    selected_friends = friends_in_group_conversations[
        friends_in_group_conversations > min_messages_to_appear
    ].index.values
    messages_in_group_conversations = messages_in_group_conversations[
        messages_in_group_conversations[messages_cols.sender].isin(selected_friends)
    ]

    participants_list_by_conversation = messages_in_group_conversations.groupby(
        messages_cols.conversation
    )[messages_cols.sender].unique()

    messages_by_person_by_conversation = messages_in_group_conversations.groupby(
        [messages_cols.conversation, messages_cols.sender]
    )[messages_cols.timestamp].count()
    total_messages_by_person = messages_in_group_conversations.groupby(
        [messages_cols.sender]
    )[messages_cols.timestamp].count()

    print("Counting common conversation messages for all friends...")
    co_occurrence = pd.DataFrame(0, index=selected_friends, columns=selected_friends)
    for conversation in tqdm(participants_list_by_conversation.index):
        participants = participants_list_by_conversation[conversation]
        messages_by_person = messages_by_person_by_conversation[conversation]
        for participant1 in range(len(participants)):
            for participant2 in range(participant1, len(participants)):
                exchanged_messages = (
                    messages_by_person[participants[participant1]]
                    + messages_by_person[participants[participant2]]
                )
                co_occurrence.loc[
                    participants[participant1], participants[participant2]
                ] += exchanged_messages
                if participant1 != participant2:
                    co_occurrence.loc[
                        participants[participant2], participants[participant1]
                    ] += exchanged_messages
    print()
    print("Adjusting for total number of messages...")
    with tqdm(total=len(selected_friends) ** 2) as pbar:
        for friend1 in selected_friends:
            for friend2 in selected_friends:
                co_occurrence.loc[friend1, friend2] = co_occurrence.loc[
                    friend1, friend2
                ] / (
                    total_messages_by_person[friend1]
                    + total_messages_by_person[friend2]
                )
                pbar.update()

    distance = 1 - co_occurrence
    return distance


@cached("projection_coordinates.db")
def get_projection_coordinates(distance):
    mds = MDS(n_components=2, verbose=1, n_jobs=-1, dissimilarity="precomputed")
    coordinates = mds.fit_transform(distance.values)

    return pd.DataFrame(coordinates, index=distance.index)


@save_graph("friends_graph")
def friends_plot(coordinates):
    _, ax = plt.subplots()
    coordinates.plot(0, 1, kind="scatter", ax=ax)

    for k, v in coordinates.iterrows():
        ax.annotate(k, v)

    return ax


@save_graph("friends_network")
def friends_network(distance, threshold):
    graph = nx.convert_matrix.from_pandas_adjacency(distance < threshold)
    _, ax = plt.subplots()
    nx.draw(graph, ax=ax)
    return ax
