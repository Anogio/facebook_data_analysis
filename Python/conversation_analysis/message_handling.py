import numpy as np
import pandas as pd

from Python.tools.data_getter import get_conversations
from Python.tools.helpers import cached


@cached('messages.db')
def generate_messages_dataframe(conversations):
    messages_df = pd.DataFrame()
    print('Generating dataframe to store all messages...')
    for conversation in conversations:
        conversation_df = pd.DataFrame(conversation['messages'])
        if 'title' in conversation:
            conversation_df['conversation_name'] = conversation['title']
        else:
            conversation_df['conversation_name'] = np.nan
        if 'sender_name' not in conversation_df.columns:
            conversation_df['sender_name'] = np.nan

        messages_df = messages_df.append(conversation_df[['conversation_name', 'sender_name', 'timestamp_ms']])
    print('Done.')
    print()
    return messages_df


def add_conversation_activity_ratio(messages_df):
    return messages_df


def get_messages_with_post_treatment():
    conversations = get_conversations()
    messages_df = generate_messages_dataframe(conversations)
    messages_df = add_conversation_activity_ratio(messages_df)

    return messages_df
