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
def top_people_graph(messages_df, my_name, top_n):
    n_messages_by_person = messages_df.groupby('sender_name')['timestamp_ms'].count().drop(my_name).rename('n_messages')
    n_messages_by_person = n_messages_by_person.sort_values().iloc[-top_n:]

    return n_messages_by_person.plot(kind='barh', x='sender_name', y='n_messages')
