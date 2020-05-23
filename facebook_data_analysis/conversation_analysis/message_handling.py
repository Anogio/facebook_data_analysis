import ftfy
import pandas as pd
from facebook_data_analysis.global_vars import messages_cols
from facebook_data_analysis.tools.data_getter import get_conversations
from facebook_data_analysis.tools.helpers import cached
from facebook_data_analysis.tools.helpers import timestamp_to_local_date


@cached("messages.db")
def generate_messages_dataframe(conversations):
    messages_df = pd.DataFrame()
    print("Generating dataframe to store all messages...")
    for conversation in conversations:
        conversation_df = pd.DataFrame(conversation["messages"])
        if "title" in conversation:
            conversation_df[messages_cols.conversation] = conversation["title"]
        else:
            conversation_df[messages_cols.conversation] = ""
        if "thread_path" in conversation:
            conversation_df[messages_cols.conv_id] = conversation["thread_path"]
        else:
            conversation_df[messages_cols.conv_id] = ""
        if messages_cols.sender not in conversation_df.columns:
            conversation_df[messages_cols.sender] = ""

        messages_df = messages_df.append(
            conversation_df[
                [
                    messages_cols.conversation,
                    messages_cols.sender,
                    messages_cols.timestamp,
                    messages_cols.conv_id,
                ]
            ]
        )
    print("Converting timestamps to dates...")
    messages_df[messages_cols.date] = messages_df[messages_cols.timestamp].apply(
        timestamp_to_local_date
    )

    print("Fixing text encoding...")
    messages_df[messages_cols.conversation] = messages_df[
        messages_cols.conversation
    ].apply(ftfy.fix_text)
    messages_df[messages_cols.sender] = messages_df[messages_cols.sender].apply(
        ftfy.fix_text
    )

    print()
    return messages_df


def conversation_stats(messages_df, my_name):
    total_messages_by_conversation = (
        messages_df.groupby(messages_cols.conv_id)[messages_cols.timestamp]
        .count()
        .rename("n_messages")
    )
    my_messages_by_conversation = (
        messages_df[messages_df[messages_cols.sender] == my_name]
        .groupby(messages_cols.conv_id)[messages_cols.timestamp]
        .count()
    )

    my_participation_by_conversation = (
        (my_messages_by_conversation / total_messages_by_conversation)
        .rename("my_participation_ratio")
        .fillna(0)
    )
    n_participants_by_conversation = (
        messages_df.groupby(messages_cols.conv_id)[messages_cols.sender]
        .nunique()
        .rename("n_participants")
    )

    my_involvement_by_conversation = (
        n_participants_by_conversation * my_participation_by_conversation
    ).rename("my_relative_participation")

    return pd.concat(
        [
            my_participation_by_conversation,
            n_participants_by_conversation,
            my_involvement_by_conversation,
            total_messages_by_conversation,
        ],
        axis=1,
    ).reset_index()


def get_messages_with_post_treatment(my_name, data_folder):
    conversations = get_conversations(data_folder)
    messages_df = generate_messages_dataframe(conversations)
    conversations_stat_df = conversation_stats(messages_df, my_name)

    return messages_df, conversations_stat_df