import numpy as np
import requests
from time import perf_counter

def greedy(container_coordinates):
    best_order = []
    best_length = float('inf')

    for i_start, start in enumerate(container_coordinates):
        order = [i_start]
        length = 0

        i_next, next_container, dist = get_closest(start, container_coordinates, order)
        length += dist
        order.append(i_next)

        while len(order) < container_coordinates.shape[0]:
            i_next, next_container, dist = get_closest(next_container, container_coordinates, order)
            length += dist
            order.append(i_next)

        if length < best_length:
            best_length = length
            best_order = order
            
    return best_order, best_length

def get_closest(container, container_coordinates, visited):
    best_distance = float('inf')

    for i, c in enumerate(container_coordinates):
        if i not in visited:
            distance = get_dist_p2p(container, c)

            if distance < best_distance:
                closest_container = c
                i_closest_container = i
                best_distance = distance

    return i_closest_container, closest_container, best_distance

def get_dist_p2p(point_start, point_end):
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
    list_of_lists = []
    with open(file_path_input, 'r') as file:
        for line in file:
            coordinates = [coord.strip() for coord in line.split(',')]
            coordinates = list(filter(None, coordinates))
            list_of_lists.append(coordinates)
    array_coordinates = np.array(list_of_lists)
    return array_coordinates

def two_opt_swap(route, i, k):
    # Perform 2-opt swap between indices i and k in the route
    new_route = route[:i] + route[i:k+1][::-1] + route[k+1:]
    return new_route

def two_opt(file_name):
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
    # Calculate the total length of the route
    length = 0
    for i in range(len(route) - 1):
        start = container_coordinates[route[i]]
        end = container_coordinates[route[i + 1]]
        length += get_dist_p2p(start, end)
    return length
    
def main(file_name):
    t1_start = perf_counter()
    best_order, best_length = two_opt(file_name)
    t1_stop = perf_counter()

    print("Runtime:", t1_stop - t1_start, "seconds")
    print("Best order:", best_order)
    print("Best length:", best_length)
    print("DONE!!")

main("Sort_algo\Coordinates_for_test\Realistic_coordinates.txt")
