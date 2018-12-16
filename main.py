import time
import os
from Python.conversation_analysis.activity_graphs import top_people_graph, all_messages_over_time, one_person_graphs
from Python.conversation_analysis.friends_network import get_people_distances, get_projection_coordinates, friends_plot, \
    friends_network
from Python.conversation_analysis.message_handling import get_messages_with_post_treatment
from Python.ip_locations_map.ip_location_tools import get_all_coordinates
from Python.ip_locations_map.ip_map import make_map

MY_NAME = 'Antoine Ogier'

t0 = time.time()
# IP location map
coordinates = get_all_coordinates()
make_map(coordinates)

# Conversation analysis
## Boilerplate to get messages info
messages_df, conversation_stat_df = get_messages_with_post_treatment(MY_NAME)
## Activity graphs
print('Generating top people graph...')
top_people_graph(messages_df, conversation_stat_df, MY_NAME, top_n=30)
print('Generating messages by week graph...')
# all_messages_over_time(messages_df, '7d')

print('Generating single person graphs')
detail_on = 'Teven Le Scao'
one_person_graphs(messages_df, detail_on)
print()

print('Generating co-occurrence graph')
distances = get_people_distances(messages_df, conversation_stat_df)
coordinates = get_projection_coordinates(distances)
friends_plot(coordinates)
friends_network(distances, 0.5)
print('Analysis completed in {time:.2f}s'.format(time=time.time() - t0))
