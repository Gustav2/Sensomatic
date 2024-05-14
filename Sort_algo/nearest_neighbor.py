import numpy
from time import perf_counter
import requests


def nearest_neighbor(d):
    """
    Nearest neighbor solver for the Traveling Salesman Problem (TSP).

    Args:
        d (NDarray): Multi-dimensional array representing the distances between nodes.
                     Example: numpy.array([[1,20,30],[5,4,2],[3,2,2]]) 
                              or numpy.array([[1,20],[5,4]])

    Returns:
        NDarray: Sorted array containing the path.
        int: Runtime in seconds.
    """
    start_timer = perf_counter() 
    
    n = d.shape[0]  # Get the number of nodes
    idx = numpy.arange(n) # Create an index array [0, 1, 2, ..., n-1]
    path = numpy.empty(n, dtype=int) # Create an empty array to store the path
    mask = numpy.ones(n, dtype=bool)  # Create a mask array initialized with True values

# Start from the first node (index 0)
    last_idx = 0
    path[0] = last_idx
    mask[last_idx] = False
    
    # Iterate through the remaining nodes to find the nearest neighbor
    for k in range(1, n):
        last_idx = idx[mask][numpy.argmin(d[last_idx, mask])]  # Find the nearest neighbor from the current node
        path[k] = last_idx # Add the nearest neighbor to the path
        mask[last_idx] = False # Update the mask to mark the nearest neighbor as visited
        
    stop_timer = perf_counter()
    runtime = stop_timer-start_timer
    
    return path, runtime


url = "https://faauzite.com/route"
query = {
  "key": "YOUR_API_KEY_HERE"
}
payload = {
  "profile": "car",
  "points": [
    [
        9.944435,
        57.029577
     
    ],
    [
        9.984215,
        57.015399
      
    ]
  ]
}
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers, params=query)
data = response.json() # data is dict type
data_list = data.get("paths") # get data in list type
data_string = "".join(str(x) for x in data_list) #convert list -> str
data_select = data_string[13:21] # select distance in meters
print(data_select)

#graph = numpy.random.rand(100,100)

#print(nearest_neighbor(graph))
