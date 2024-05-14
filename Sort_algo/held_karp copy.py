import itertools
import random
from time import perf_counter
import requests

def held_karp(dists):
    """
    Held-Karp algorithm to solve the Traveling Salesman Problem (TSP)
    using dynamic programming with memoization.

    Parameters:
        dists (list of lists): Distance matrix representing distances between nodes.

    Returns:
        tuple: A tuple containing the optimal cost and the path.
    """
    n = len(dists)

    # Dictionary to store the cost and parent node for each subset of nodes.
    # Node subsets are represented using set bits.
    C = {}

    # Set transition cost from the initial state
    for k in range(1, n):
        # For each node k, store the cost to reach k from the initial state (0) and the parent node (0)
        C[(1 << k, k)] = (dists[0][k], 0)

    # Iterate over subsets of increasing length and store intermediate results
    for subset_size in range(2, n):
        # Generate all combinations of nodes of size subset_size
        for subset in itertools.combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to reach this subset
            for k in subset:               
                prev = bits & ~(1 << k) # Compute the bits for the subset without node k

                # Calculate the cost to reach node k from each node m in the subset
                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m)) # Cost to reach node k = cost to reach node m + distance from m to k
                C[(bits, k)] = min(res) # Store the minimum cost and the parent node for the subset and node k

    # Calculate the optimal cost starting from the full set of nodes
    bits = (2**n - 1) - 1
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k)) # Cost to reach the start node (0) from node k
    
    opt, parent = min(res) # Find the minimum cost and the parent node

    # Backtrack to find the full path
    path = []
    for i in range(n - 1):
        path.append(parent)
        # Update the bits to exclude the parent node
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    path.append(0) # Add the implicit start state

    return opt, list(reversed(path))

def generate_distances(n):
    """
    Generate a random distance matrix for a given number of nodes.

    Parameters:
        n (int): Number of nodes.

    Returns:
        list of lists: Distance matrix.
    """
    dists = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            # Generate random distances between 1 and 99
            dists[i][j] = dists[j][i] = random.randint(1, 99)

    return dists

# latitude(north(+), south(-)), longitude(east(+), west(-)) -> when (+) no indicator only if (-)
def get_dist_p2p(start_latitude_input, start_longitude_input, end_latitude_input, end_longitude_input):
    
    start_latitude = start_latitude_input
    start_longitude = start_longitude_input
    end_latitude = end_latitude_input
    end_longitude = end_longitude_input
    
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
    data = response.json() # data is dict type
    data_list = data.get("paths") # get data in list type
    data_string = "".join(str(x) for x in data_list) # convert list -> str
    data_select = data_string[13:21] # select distance in meters from str
    return(data_select)

def select_coordinates(file_path_input):
    file_path = file_path_input
    list_of_lists = []
    with open(file_path, 'r') as file:
        for line in file:
            list_of_lists.append(line.strip().split(','))
    return list_of_lists

def make_dist_matrix():
    tal = 0
    master_coordinate_list = select_coordinates("Sort_algo\coordinates.txt")
    dists = [[0] * len(master_coordinate_list) for i in range(len(master_coordinate_list))]
    for i in range(len(master_coordinate_list)):
        print(tal)
        for n in range(len(master_coordinate_list)):
            
            point_start = master_coordinate_list[i-1]
            point_end = master_coordinate_list[n-1]
            start_latitude = float(point_start[0])
            start_longitude = float(point_start[1])
            end_latitude = float(point_end[0])
            end_longitude = float(point_end[1])
            tal = tal + 1
            #print(tal)
            #print(f"n: {n}, i: {i}: {start_latitude}, {start_longitude}, {end_latitude}, {end_longitude}")
            dist_p2p = get_dist_p2p(start_longitude, start_latitude, end_longitude, end_latitude)
            #print(dist_p2p)
    print(tal)


#print(get_dist_p2p(57.029577,9.944435, 57.015399,9.984215))
#t1_start = perf_counter() # Start the timer
#make_dist_matrix()
#t1_stop = perf_counter() # Stop the timer
#print("Runtime:", t1_stop - t1_start, "seconds")


"""
distances = generate_distances(10) # Generate a distance matrix for nodes

t1_start = perf_counter() # Start the timer

result = held_karp(distances) # Run Held-Karp algorithm on the generated distance matrix

t1_stop = perf_counter() # Stop the timer
"""

# Print the result and the runtime
#print("Distance matrix", distances)
#print("Optimal Cost:", result[0])
#print("Optimal Path:", result[1])
#print("Runtime:", t1_stop - t1_start, "seconds")
