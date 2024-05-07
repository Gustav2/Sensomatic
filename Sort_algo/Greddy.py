import numpy as np
import requests
from time import perf_counter

def algorithm(cities):
    best_order = []
    best_length = float('inf')

    for i_start, start in enumerate(cities):
        print("YES")
        order = [i_start]
        length = 0

        i_next, next_city, dist = get_closest(start, cities, order)
        length += dist
        order.append(i_next)

        while len(order) < cities.shape[0]:
            i_next, next_city, dist = get_closest(next_city, cities, order)
            length += dist
            order.append(i_next)

        if length < best_length:
            best_length = length
            best_order = order
            
    return best_order, best_length

def get_closest(city, cities, visited):
    best_distance = float('inf')

    for i, c in enumerate(cities):
        if i not in visited:
            distance = get_dist_p2p(city, c)

            if distance < best_distance:
                closest_city = c
                i_closest_city = i
                best_distance = distance

    return i_closest_city, closest_city, best_distance

def dist_squared(c1, c2):
    t1 = c2[0] - c1[0]
    t2 = c2[1] - c1[1]

    return t1**2 + t2**2

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
        [
            start_longitude, 
            start_latitude
        
        ],
        [
            end_longitude,
            end_latitude
        
        ]
    ]
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, params=query)
    data_dict_level0 = response.json()
    data_dict_level1 = data_dict_level0["paths"]
    data_dict_level2 = data_dict_level1[0]
    data_final = data_dict_level2["distance"]
    #print(data_final)
    
    return(data_final)

def select_coordinates(file_path_input):
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
    return array_coordinates


def main():
    t1_start = perf_counter() # Start the timer

    cities = select_coordinates("Sort_algo\Realistic_coordinates.txt")
    print(len(cities))
    best_order, best_length = algorithm(cities)
    
    t1_stop = perf_counter() # Stop the timer

    # Print the best order and length
    print("Runtime:", t1_stop - t1_start, "seconds")
    print("Best order:", best_order)
    print("Best length:", best_length)

 
main()



# Example input: Cities represented as coordinates (x, y)
#cities = np.array([[0, 0], [1, 2], [3, 1], [2, 3]])


