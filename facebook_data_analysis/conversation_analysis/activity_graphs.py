import pandas as pd
from facebook_data_analysis.global_vars import messages_cols
from facebook_data_analysis.tools.helpers import OUTPUT_FOLDER
from facebook_data_analysis.tools.helpers import resolve_path


def save_graph(file_name):
    def decorator(wrapped):
        def decorated(*args, **kwargs):
            res = wrapped(*args, **kwargs)
            fig = res.get_figure()

            file_path = resolve_path(OUTPUT_FOLDER, file_name)
            fig.savefig(file_path, bbox_inches="tight")
            return res

        return decorated

    return decorator


def save_graphs(file_names):
    def decorator(wrapped):
        def decorated(*args, **kwargs):
            res = wrapped(*args, **kwargs)
            for i, file_name in enumerate(file_names):
                file_path = resolve_path(OUTPUT_FOLDER, file_name)
                fig = res[i].get_figure()
                fig.savefig(file_path, bbox_inches="tight")
            return res

        return decorated

    return decorator


@save_graphs(["top_people_all_conv", "top_people_dm"])
def top_people_graph(messages_df, conversations_df, my_name, top_n):
    messages_df = pd.merge(
        messages_df, conversations_df, on=messages_cols.conv_id, how="left"
    )

    # First, get number of messages on all conversations
    messages_df["conversation_weight"] = 1 / messages_df["n_participants"]
    n_messages_by_person = (
        messages_df.groupby(messages_cols.sender)["conversation_weight"]
        .sum()
        .drop(my_name)
        .rename("n_messages_weighted_by_conversation")
    )
    n_messages_by_person = n_messages_by_person.sort_values().iloc[-top_n:]

    # Second, get number of messages on direct messages
    direct_messages_df = messages_df.loc[
        (messages_df["n_participants"] == 2) & (messages_df["sender_name"] != my_name)
    ]
    n_direct_messages_by_person = (
        direct_messages_df.groupby(messages_cols.sender)
        .size()
        .reset_index(name="n_direct_messages")
    )
    n_direct_messages_by_person = n_direct_messages_by_person.sort_values(
        by="n_direct_messages"
    ).iloc[-top_n:]

    return (
        n_messages_by_person.plot(
            kind="barh",
            x=messages_cols.sender,
            y="n_messages_weighted_by_conversation_activity",
        ),
        n_direct_messages_by_person.plot(
            kind="barh", x=messages_cols.sender, y="n_direct_messages"
        ),
    )


@save_graph("top_conversations")
def top_conv_graph(conversations_df, top_n=40):
    n_messages_by_conv = conversations_df.sort_values(by="n_messages").iloc[-top_n:]
    return n_messages_by_conv.plot(kind="barh", x=messages_cols.conv_id, y="n_messages")


@save_graph("total_messages")
def all_messages_over_time(messages_df, interval):
    messages_df = messages_df.copy()
    messages_df["one"] = 1

    amount_column_name = "n_messages_per_" + interval
    rolling_n_messages = (
        messages_df.set_index(messages_cols.date)
        .sort_index()["one"]
        .rolling(interval)
        .sum()
        .rename(amount_column_name)
        .reset_index()
    )

    return rolling_n_messages.plot(x="date", y=amount_column_name)


@save_graphs(["single_person_pie", "single_person_activity"])
def one_person_graphs(messages_df, name, interval="7d", top_n_pie=10):
    person_df = messages_df[messages_df[messages_cols.sender] == name].copy()

    messages_by_conversation = person_df.groupby(messages_cols.conversation)[
        messages_cols.sender
    ].count()
    top_messages_by_conversation = messages_by_conversation.sort_values().iloc[
        -top_n_pie:
    ]
    pie = pd.DataFrame(top_messages_by_conversation.rename("n_messages")).plot(
        kind="pie",
        y="n_messages",
        title="{} (top {} conversations)".format(name, top_n_pie),
        legend=False,
    )

    amount_column_name = "n_messages_per_" + interval
    person_df["one"] = 1
    line = (
        person_df.set_index(messages_cols.date)
        .sort_index()["one"]
        .rolling(interval)
        .sum()
        .rename(amount_column_name)
        .reset_index()
        .plot(x="date", y=amount_column_name, title=name)
    )

    return pie, line
