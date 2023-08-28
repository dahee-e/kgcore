

import os

parent_folder = "D:/Data/kg_core/real/"

# Create a list to store the organized information
organized_data = []

# Traverse through the subfolders
for subfolder in os.listdir(parent_folder):
    subfolder_path = os.path.join(parent_folder, subfolder)

    # Check if the path is a directory
    if os.path.isdir(subfolder_path):

        # Traverse through the files in the subfolder
        for file_name in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, file_name)

            # Check if the file contains "core.dat" in its name
            if "core.dat" in file_name:

                # Extract the first and second integers from the file name
                first_integer, second_integer = file_name.split("_")[:2]

                # Read the number of nodes and running time from the file
                with open(file_path, "r") as file:
                    number_of_nodes = file.readline().strip()
                    running_time = file.readline().strip()

                # Determine the Type based on the values of first_integer and second_integer
                if first_integer == "3":
                    # Set Type as 1 for k=3
                    organized_data.append(
                        [subfolder, first_integer, second_integer, number_of_nodes, running_time, "Type 1"])
                else:
                    # Set Type as 2 for varying k
                    organized_data.append(
                        [subfolder, first_integer, second_integer, number_of_nodes, running_time, "Type 2"])

                # Add an additional entry with Type 2 for the case 3, 3
                if first_integer == "3" and second_integer == "3":
                    organized_data.append(
                        [subfolder, first_integer, second_integer, number_of_nodes, running_time, "Type 2"])

# Print the organized information
for data in organized_data:
    print("\t".join(data))
