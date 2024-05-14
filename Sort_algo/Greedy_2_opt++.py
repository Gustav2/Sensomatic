
import numpy as np
import requests
from time import perf_counter

def greedy(container_coordinates, cache):
    """
    Greedy algorithm to find an initial solution for the traveling salesman problem.
    
    Args:
        container_coordinates (numpy.ndarray): Array containing coordinates of containers.
        cache (dict): Dictionary to store already calculated distances.
        
    Returns:
        tuple: A tuple containing the best order of visiting containers and the corresponding length.
    """
    best_order = []
    best_length = float('inf')

    for i_start, start in enumerate(container_coordinates):
        order = [i_start]
        length = 0

        i_next, next_container, dist = get_closest(start, container_coordinates, order, cache)
        length += dist
        order.append(i_next)

        while len(order) < container_coordinates.shape[0]:
            i_next, next_container, dist = get_closest(next_container, container_coordinates, order, cache)
            length += dist
            order.append(i_next)

        if length < best_length:
            best_length = length
            best_order = order
            
    return best_order, best_length

def get_closest(container, container_coordinates, visited, cache):
    """
    Find the closest unvisited container to a given container.
    
    Args:
        container (numpy.ndarray): Coordinates of the current container.
        container_coordinates (numpy.ndarray): Array containing coordinates of containers.
        visited (list): List of indices of visited containers.
        cache (dict): Dictionary to store already calculated distances.
        
    Returns:
        tuple: A tuple containing the index of the closest container, its coordinates, and the distance to it.
    """
    best_distance = float('inf')

    for i, c in enumerate(container_coordinates):
        if i not in visited:
            if (container.tobytes(), c.tobytes()) in cache:
                distance = cache[(container.tobytes(), c.tobytes())]
            else:
                distance = get_dist_p2p(container, c)
                cache[(container.tobytes(), c.tobytes())] = distance

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
    start_latitude = float(point_start[1])
    start_longitude = float(point_start[0])
    end_latitude = float(point_end[1])
    end_longitude = float(point_end[0])
    
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
    list_of_lists = []
    with open(file_path_input, 'r') as file:
        for line in file:
            coordinates = [coord.strip() for coord in line.split(',')]
            coordinates = list(filter(None, coordinates))
            list_of_lists.append(coordinates)
    array_coordinates = np.array(list_of_lists)
    return array_coordinates

def two_opt_plus_plus_swap(route, i, k):
    """
    Perform a 2-opt++ swap operation between two nodes in a route.

    Args:
        route (list): List representing the order of visiting containers.
        i (int): Index of the first container to swap.
        k (int): Index of the second container to swap.
        
    Returns:
        list: Updated route after performing the 2-opt++ swap.
    """
    # Create a set of all nodes in the route
    route_set = set(route)

    # Determine the neighbors of nodes i and k
    neighbors_i = get_neighbors(route, i)
    neighbors_k = get_neighbors(route, k)

    # Find the common neighbors between nodes i and k
    common_neighbors = neighbors_i.intersection(neighbors_k)

    # If there are common neighbors, select the closest one for the swap
    if common_neighbors:
        closest_common_neighbor = min(common_neighbors, key=lambda x: route.index(x))
        # Swap edges (i, i+1) and (k, k+1) with (i, k) and (i+1, k+1)
        new_route = route[:i] + [closest_common_neighbor] + route[i+1:k+1] + [route[i]] + route[k+1:]
    else:
        # If there are no common neighbors, perform a regular 2-opt swap
        new_route = two_opt_swap(route, i, k)

    return new_route

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

def two_opt_plus_plus(file_name):
    """
    Implement the 2-opt++ algorithm to optimize the route.
    
    Args:
        file_name (str): Name of the file containing container coordinates.
        
    Returns:
        best_order (list): A list containing the best order of visiting containers.
        best_length (float): Float value of the route length in meters.
    """
    container_coordinates = select_coordinates(file_name)
    cache = {}
    best_order, best_length = greedy(container_coordinates, cache)
    
    # Initialize variables for optimization loop
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best_order) - 2):
            for k in range(i + 2, len(best_order)):
                new_order = two_opt_plus_plus_swap(best_order, i, k)
                new_length = calculate_route_length(new_order, container_coordinates, cache)
                if new_length < best_length:
                    best_order = new_order
                    best_length = new_length
                    improved = True
                    break
            if improved:
                break
                
    return best_order, best_length 

def get_neighbors(route, index):
    """
    Get the set of neighboring nodes of a node in a route.
    
    Args:
        route (list): List representing the order of visiting containers.
        index (int): Index of the node.
        
    Returns:
        set: Set of neighboring nodes.
    """
    neighbors = set()
    num_nodes = len(route)
    if index > 0:
        neighbors.add(route[index - 1])
    if index < num_nodes - 1:
        neighbors.add(route[index + 1])
    return neighbors

def calculate_route_length(route, container_coordinates, cache):
    """
    Calculate the total length of a route.
    
    Args:
        route (list): List representing the order of visiting containers.
        container_coordinates (numpy.ndarray): Array containing coordinates of containers.
        cache (dict): Dictionary to store already calculated distances.
        
    Returns:
        float: Total length of the route.
    """
    length = 0
    for i in range(len(route) - 1):
        start = container_coordinates[route[i]]
        end = container_coordinates[route[i + end]]
        if (start.tobytes(), end.tobytes()) in cache:
            length += cache[(start.tobytes(), end.tobytes())]
        else:
            distance = get_dist_p2p(start, end)
            cache[(start.tobytes(), end.tobytes())] = distance
            length += distance
    return length
    
def main(file_name):
    """
    Main function to execute the 2-opt++ algorithm and print the results.
    
    Args:
        file_name (str): Name of the file containing container coordinates.
    
    Returns:
        best_order (list): A list containing the best order of visiting containers.
        best_length (float): Float value of the route length in meters.
        time_total (float): Time it took to calculate
    """
    # Start the timer
    t1_start = perf_counter()
    best_order, best_length = two_opt_plus_plus(file_name)
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
