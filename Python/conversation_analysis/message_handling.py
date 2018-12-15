import numpy as np
import pandas as pd

from Python.global_vars import messages_cols
from Python.tools.data_getter import get_conversations
from Python.tools.helpers import cached, timestamp_to_local_date
import ftfy

@cached('messages.db')
def generate_messages_dataframe(conversations):
    messages_df = pd.DataFrame()
    print('Generating dataframe to store all messages...')
    for conversation in conversations:
        conversation_df = pd.DataFrame(conversation['messages'])
        if 'title' in conversation:
            conversation_df[messages_cols.conversation] = conversation['title']
        else:
            conversation_df[messages_cols.conversation] = ''
        if messages_cols.sender not in conversation_df.columns:
            conversation_df[messages_cols.sender] = ''

        messages_df = messages_df.append(
            conversation_df[[messages_cols.conversation, messages_cols.sender, messages_cols.timestamp]])
    print('Converting timestamps to dates...')
    messages_df[messages_cols.date] = messages_df[messages_cols.timestamp].apply(timestamp_to_local_date)

    print('Fixing text encoding...')
    messages_df[messages_cols.conversation] = messages_df[messages_cols.conversation].apply(ftfy.fix_text)
    messages_df[messages_cols.sender] = messages_df[messages_cols.sender].apply(ftfy.fix_text)

    print()
    return messages_df


def conversation_stats(messages_df, my_name):
    total_messages_by_conversation = messages_df.groupby(messages_cols.conversation)[messages_cols.timestamp].count()
    my_messages_by_conversation = \
        messages_df[messages_df[messages_cols.sender] == my_name].groupby(messages_cols.conversation)[
            messages_cols.timestamp
        ].count()

    my_participation_by_conversation = (my_messages_by_conversation / total_messages_by_conversation).rename(
        'my_participation_ratio').fillna(0)
    n_participants_by_conversation = messages_df.groupby(messages_cols.conversation)[
        messages_cols.sender].nunique().rename('n_participants')

    my_involvement_by_conversation = (n_participants_by_conversation * my_participation_by_conversation).rename(
        'my_relative_participation')
    return pd.concat([my_participation_by_conversation, n_participants_by_conversation, my_involvement_by_conversation],
                     axis=1).reset_index()


def get_messages_with_post_treatment(my_name):
    conversations = get_conversations()
    messages_df = generate_messages_dataframe(conversations)
    conversations_stat_df = conversation_stats(messages_df, my_name)

    return messages_df, conversations_stat_df
