"""Script that uses a Greddy-2-opt hyprid algorithem to make an optimal route for garbage truck
    to be more effecient when emptying containers in inner Aalborg

Returns:
    list: If "main" function is run the main return is a sorted list (there are other returns as well).
"""

import numpy as np
import requests
from time import perf_counter

def greedy(container_coordinates):
    """
    Greedy algorithm to find an initial solution for the traveling salesman problem.
    
    Args:
        container_coordinates (numpy.ndarray): Array containing coordinates of containers.
        
    Returns:
        tuple: A tuple containing the best order of visiting containers and the corresponding length.
    """
    # Initialize variables to store the best order and length
    best_order = []
    best_length = float('inf')

    # Loop through each container as a starting point
    for i_start, start in enumerate(container_coordinates):
        # Initialize the order of containers and total length
        order = [i_start]
        length = 0

        # Find the closest container to the current container
        i_next, next_container, dist = get_closest(start, container_coordinates, order)
        length += dist
        order.append(i_next)

        # Continue adding containers until all are visited
        while len(order) < container_coordinates.shape[0]:
            i_next, next_container, dist = get_closest(next_container, container_coordinates, order)
            length += dist
            order.append(i_next)

        # Update the best order and length if a shorter path is found
        if length < best_length:
            best_length = length
            best_order = order
            
    return best_order, best_length

def get_closest(container, container_coordinates, visited):
    """
    Find the closest unvisited container to a given container.
    
    Args:
        container (numpy.ndarray): Coordinates of the current container.
        container_coordinates (numpy.ndarray): Array containing coordinates of containers.
        visited (list): List of indices of visited containers.
        
    Returns:
        tuple: A tuple containing the index of the closest container, its coordinates, and the distance to it.
    """
    # Initialize the best distance to infinity
    best_distance = float('inf')

    # Loop through each container
    for i, c in enumerate(container_coordinates):
        # Check if the container has not been visited
        if i not in visited:
            # Calculate the distance between the current container and the next container
            distance = get_dist_p2p(container, c)

            # Update the closest container if a shorter distance is found
            if distance < best_distance:
                closest_container = c
                i_closest_container = i
                best_distance = distance

    return i_closest_container, closest_container, best_distance

def get_dist_p2p(point_start, point_end):
    """
    Calculate the distance between two points using API.
    
    Args:
        point_start (numpy.ndarray): Coordinates of the starting point.
        point_end (numpy.ndarray): Coordinates of the ending point.
        
    Returns:
        float: The distance between the two points.
    """
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
    """
    Read container coordinates from a file.
    
    Args:
        file_path_input (str): Path to the input file containing container coordinates.
        
    Returns:
        numpy.ndarray: Array containing container coordinates.
    """
    # Read coordinates from a file and convert them to a NumPy array
    list_of_lists = []
    with open(file_path_input, 'r') as file:
        for line in file:
            # Split the line by comma and remove leading/trailing whitespace from each element
            coordinates = [coord.strip() for coord in line.split(',')]
            # Remove empty strings from the list of coordinates
            coordinates = list(filter(None, coordinates))
            list_of_lists.append(coordinates)
    array_coordinates = np.array(list_of_lists)
    return array_coordinates



def two_opt_swap(route, i, k):
    """
    Perform a 2-opt swap operation between two nodes in a route.
    
    Args:
        route (list): List representing the order of visiting containers.
        i (int): Index of the first container to swap.
        k (int): Index of the second container to swap.
        
    Returns:
        list: Updated route after performing the 2-opt swap.
    """
    # Perform 2-opt swap between indices i and k in the route
    new_route = route[:i] + route[i:k+1][::-1] + route[k+1:]
    return new_route

def two_opt(file_name):
    """
    Implement the 2-opt algorithm to optimize the route.
    
    Args:
        file_name (str): Name of the file containing container coordinates.
        
    Returns:
        best_order (list): A list containing the best order of visiting containers.
        best_length (float): Float value of the route length in meters.
    """
    # Execute the two-opt algorithm to optimize the route
    container_coordinates = select_coordinates(file_name)
    best_order, best_length = greedy(container_coordinates)
    
    # Initialize variables for optimization loop
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best_order) - 1):
            for k in range(i + 1, len(best_order)):
                new_order = two_opt_swap(best_order, i, k)
                new_length = calculate_route_length(new_order, container_coordinates)
                if new_length < best_length:
                    best_order = new_order
                    best_length = new_length
                    improved = True
                    break
            if improved:
                break
                
    return best_order, best_length 

def calculate_route_length(route, container_coordinates):
    """
    Calculate the total length of a route.
    
    Args:
        route (list): List representing the order of visiting containers.
        container_coordinates (numpy.ndarray): Array containing coordinates of containers.
        
    Returns:
        float: Total length of the route.
    """
    # Calculate the total length of the route
    length = 0
    for i in range(len(route) - 1):
        start = container_coordinates[route[i]]
        end = container_coordinates[route[i + 1]]
        length += get_dist_p2p(start, end)
    return length
    
def main(file_name):
    """
    Main function to execute the 2-opt algorithm and print the results.
    
    Args:
        file_name (str): Name of the file containing container coordinates.
    
    Returns:
        best_order (list): A list containing the best order of visiting containers.
        best_length (float): Float value of the route length in meters.
        time_total (float): Time it took to calculate
    """
    # Start the timer
    t1_start = perf_counter()
    best_order, best_length = two_opt(file_name)
    # Stop the timer
    t1_stop = perf_counter()

    time_total = t1_stop - t1_start
    
    # Print the runtime, best order, and best length
    """
    print("Runtime:", time_total, "seconds")
    print("Best order:", best_order)
    print("Best length:", best_length)
    print("DONE!!")
    """
    
    return best_order, best_length, time_total

def get_full_containers():
    #IMPORT FROM DB
    pass