import argparse
import os
import shutil
import time

from facebook_data_analysis.conversation_analysis.activity_graphs import (
    all_messages_over_time,
)
from facebook_data_analysis.conversation_analysis.activity_graphs import (
    one_person_graphs,
)
from facebook_data_analysis.conversation_analysis.activity_graphs import top_conv_graph
from facebook_data_analysis.conversation_analysis.activity_graphs import (
    top_people_graph,
)
from facebook_data_analysis.conversation_analysis.friends_network import friends_network
from facebook_data_analysis.conversation_analysis.friends_network import friends_plot
from facebook_data_analysis.conversation_analysis.friends_network import (
    get_people_distances,
)
from facebook_data_analysis.conversation_analysis.friends_network import (
    get_projection_coordinates,
)
from facebook_data_analysis.conversation_analysis.message_handling import (
    get_messages_with_post_treatment,
)
from facebook_data_analysis.ip_locations_map.ip_location_tools import (
    get_all_coordinates,
)
from facebook_data_analysis.ip_locations_map.ip_map import make_map
from facebook_data_analysis.tools.helpers import output_path


if __name__ == "__main__":
    # Get the arguments of the script
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", type=str, required=True)
    parser.add_argument("-n", "--facebook_name", type=str)
    command_line_args = parser.parse_args()

    MY_NAME = command_line_args.facebook_name or input("Your exact facebook name: ")
    data_folder = command_line_args.folder

    # Create the folder for the outputs
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    else:
        confirm = ""
        while confirm not in ["y", "n"]:
            confirm = input(
                "A cache is present from a previous run. Do you want to keep it ? (y/n)"
            ).lower()
            if confirm == "n":
                shutil.rmtree(output_path)
                os.makedirs(output_path)

    t0 = time.time()
    # IP location map
    coordinates = get_all_coordinates(data_folder)
    make_map(coordinates)

    # Conversation analysis
    # Boilerplate to get messages info
    messages_df, conversation_stat_df = get_messages_with_post_treatment(
        MY_NAME, data_folder
    )
    # Activity graphs
    print("Generating top people graph...")
    top_people_graph(messages_df, conversation_stat_df, MY_NAME, top_n=30)
    print("Generating messages by week graph...")
    all_messages_over_time(messages_df, "7d")

    print("Generating all conversations graphs")
    top_conv_graph(conversation_stat_df)
    print()

    print("Generating single person graphs")
    detail_on = "Teven Le Scao"
    one_person_graphs(messages_df, detail_on)
    print()

    print("Generating co-occurrence graph")
    distances = get_people_distances(messages_df, conversation_stat_df)
    coordinates = get_projection_coordinates(distances)
    friends_plot(coordinates)
    friends_network(distances, 0.5)
    print("Analysis completed in {time:.2f}s".format(time=time.time() - t0))
