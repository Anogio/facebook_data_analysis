import pandas as pd

from Python.global_vars import messages_cols
from Python.tools.helpers import resolve_path, OUTPUT_FOLDER


def save_graph(file_name):
    def decorator(wrapped):
        def decorated(*args, **kwargs):
            res = wrapped(*args, **kwargs)
            fig = res.get_figure()

            file_path = resolve_path(OUTPUT_FOLDER, file_name)
            fig.savefig(file_path, bbox_inches='tight')
            return res

        return decorated

    return decorator


@save_graph('top_people.pdf')
def top_people_graph(messages_df, conversations_df, my_name, top_n):
    messages_df = pd.merge(messages_df, conversations_df, on=messages_cols.conversation, how='left')

    messages_df['conversation_weight'] = 1 / messages_df['n_participants']
    n_messages_by_person = messages_df.groupby(messages_cols.sender)['conversation_weight'].sum().drop(my_name).rename(
        'n_messages_weighted_by_conversation')
    n_messages_by_person = n_messages_by_person.sort_values().iloc[-top_n:]

    return n_messages_by_person.plot(kind='barh', x=messages_cols.sender,
                                     y='n_messages_weighted_by_conversation_activity')
