from Python.conversation_analysis.activity_graphs import top_people_graph
from Python.conversation_analysis.message_handling import get_messages_with_post_treatment
from Python.ip_locations_map.ip_location_tools import get_all_coordinates
from Python.ip_locations_map.ip_map import make_map

MY_NAME = 'Antoine Ogier'

# IP location map
coordinates = get_all_coordinates()
make_map(coordinates)

# Conversation analysis
## Boilerplate to get messages info
messages_df, conversation_stat_df = get_messages_with_post_treatment(MY_NAME)
## Activity graphs
top_people_graph(messages_df, conversation_stat_df, MY_NAME, top_n=30)
