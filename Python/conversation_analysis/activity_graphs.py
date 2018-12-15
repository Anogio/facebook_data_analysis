import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


def get_messages_dataframe(conversations):
    if os.path.isfile('messages.hdf'):
        print('Retrieving existing messages dataframe...')
        messages_df = pd.read_hdf('messages.hdf')
        print('Done.')
        print()
        return messages_df
    messages_df = generate_messages_dataframe(conversations)
    messages_df.to_hdf('messages.hdf', 'messages')
    return messages_df


def top_people_graph(messages_df, my_name, top_n):
    n_messages_by_person = messages_df.groupby('sender_name')['timestamp_ms'].count().drop(my_name).rename('n_messages')
    n_messages_by_person = n_messages_by_person.sort_values().iloc[-top_n:]

    n_messages_by_person.plot(kind='barh', x='sender_name', y='n_messages')
    plt.show()
