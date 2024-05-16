import numpy as np
import requests
from time import perf_counter

def algorithm(containere_coordinates):
    # Initialize variables to store the best order and length
    best_order = []
    best_length = float('inf')

    # Loop through each containere as a starting point
    for i_start, start in enumerate(containere_coordinates):
        # Initialize the order of containeres and total length
        order = [i_start]
        length = 0

        # Find the closest containere to the current containere
        i_next, next_containere, dist = get_closest(start, containere_coordinates, order)
        length += dist
        order.append(i_next)

        # Continue adding cities until all are visited
        while len(order) < containere_coordinates.shape[0]:
            i_next, next_containere, dist = get_closest(next_containere, containere_coordinates, order)
            length += dist
            order.append(i_next)

        # Update the best order and length if a shorter path is found
        if length < best_length:
            best_length = length
            best_order = order
            
    return best_order, best_length

def get_closest(containere, containere_coordinates, visited):
    # Initialize the best distance to infinity
    best_distance = float('inf')

    # Loop through each containere
    for i, c in enumerate(containere_coordinates):
        # Check if the containere has not been visited
        if i not in visited:
            # Calculate the distance between the current containere and the next containere
            distance = get_dist_p2p(containere, c)

            # Update the closest containere if a shorter distance is found
            if distance < best_distance:
                closest_containere = c
                i_closest_containere = i
                best_distance = distance

    return i_closest_containere, closest_containere, best_distance

def get_dist_p2p(point_start, point_end):
    # Extract latitude and longitude coordinates for start and end points
    start_latitude = float(point_start[1])
    start_longitude = float(point_start[0])
    end_latitude = float(point_end[1])
    end_longitude = float(point_end[0])
    
    # Set up the API request to calculate the distance between two points
    url = "https://faauzite.com/route"
    query = {
        "key": "YOUR_API_KEY_HERE" 
    }
    payload = {
        "profile": "car",
        "points": [
            [start_longitude, start_latitude],
            [end_longitude, end_latitude]
        ]
    }
    
    # Make the API request and parse the response to extract the distance
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, params=query)
    data_dict_level0 = response.json()
    data_dict_level1 = data_dict_level0["paths"]
    data_dict_level2 = data_dict_level1[0]
    data_final = data_dict_level2["distance"]
    
    return data_final

def select_coordinates(file_path_input):
    # Read coordinates from a file and convert them to a NumPy array
    file_path = file_path_input
    list_of_lists = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by comma and remove leading/trailing whitespace from each element
            coordinates = [coord.strip() for coord in line.split(',')]
            # Remove empty strings from the list of coordinates
            coordinates = list(filter(None, coordinates))
            list_of_lists.append(coordinates)
    print(list_of_lists)
    
    array_coordinates = np.array(list_of_lists)
    print(array_coordinates.shape)
    return array_coordinates

def main():
    # Start the timer
    t1_start = perf_counter()

    # Read containeres from a file and find the shortest path
    containere_coordinates = select_coordinates("Sort_algo\Coordinates_for_test\coordinates_5.txt")
    print(len(containere_coordinates))
    best_order, best_length = algorithm(containere_coordinates)
    
    # Stop the timer
    t1_stop = perf_counter()

    # Print the runtime, best order, and best length
    print("Runtime:", t1_stop - t1_start, "seconds")
    print("Best order:", best_order)
    print("Best length:", best_length)

main()