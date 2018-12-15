import operator

from Python.conversation_analysis.activity_graphs import top_people_graph, get_messages_dataframe, add_conversation_activity_ratio
from Python.tools.data_getter import get_conversations

MY_NAME = 'Antoine Ogier'

# coordinates = get_all_coordinates()
# make_map(coordinates)

conversations = get_conversations()
messages_df = get_messages_dataframe(conversations)
messages_df = add_conversation_activity_ratio(messages_df)
top_people_graph(messages_df, MY_NAME, 30)

