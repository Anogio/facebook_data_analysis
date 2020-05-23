import argparse
import os
import shutil
import time

from facebook_data_analysis.conversation_analysis import activity_graphs
from facebook_data_analysis.conversation_analysis import friends_network
from facebook_data_analysis.conversation_analysis import message_handling
from facebook_data_analysis.ip_locations_map import ip_location_tools
from facebook_data_analysis.ip_locations_map import ip_map
from facebook_data_analysis.tools import helpers


if __name__ == "__main__":
    # Get the arguments of the script
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", type=str, required=True)
    parser.add_argument("-n", "--facebook_name", type=str)
    command_line_args = parser.parse_args()

    MY_NAME = command_line_args.facebook_name or input("Your exact facebook name: ")
    data_folder = command_line_args.folder

    # Create the folder for the outputs
    if not os.path.isdir(helpers.output_path):
        os.makedirs(helpers.output_path)

    if os.path.isdir(helpers.cache_path):
        confirm = ""
        while confirm not in ["y", "n"]:
            confirm = input(
                "A cache is present from a previous run. Do you want to keep it ? (y/n): "
            ).lower()
            if confirm == "n":
                print("Resetting cache...")
                shutil.rmtree(helpers.cache_path)

    t0 = time.time()
    # IP location map
    coordinates = ip_location_tools.get_all_coordinates(data_folder)
    ip_map.make_map(coordinates)

    # Conversation analysis
    # Boilerplate to get messages info
    messages_df, conversation_stat_df = message_handling.get_messages_with_post_treatment(
        MY_NAME, data_folder
    )
    # Activity graphs
    print("Generating top people graph...")
    activity_graphs.top_people_graph(
        messages_df, conversation_stat_df, MY_NAME, top_n=30
    )
    print("[SKIPPING] Generating messages by week graph...")
    # all_messages_over_time(messages_df, "7d")

    print("Generating all conversations graphs")
    activity_graphs.top_conv_graph(conversation_stat_df)
    print()

    print("Generating single person graphs")
    detail_on = "Teven Le Scao"
    activity_graphs.one_person_graphs(messages_df, detail_on)
    print()

    print("Generating co-occurrence graph")
    distances = friends_network.get_people_distances(messages_df, conversation_stat_df)
    coordinates = friends_network.get_projection_coordinates(distances)
    friends_network.friends_plot(coordinates)
    friends_network.friends_network(distances, 0.5)
    print("Analysis completed in {time:.2f}s".format(time=time.time() - t0))
