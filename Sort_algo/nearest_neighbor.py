import numpy
from time import perf_counter_ns


def nearest_neighbor(d):
    """nearest neighbor solver for TSP 

    Args:
        d (NDarray): Multi dimentional array. Ex: numpy.array([[1,20,30],[5,4,2],[3,2,2]]) or numpy.array([[1,20],[5,4]])

    Returns:
        NDarray: Sortet array.
    """
    start_timer = perf_counter_ns()
    
    n = d.shape[0]
    idx = numpy.arange(n)
    path = numpy.empty(n, dtype=int)
    mask = numpy.ones(n, dtype=bool)

    last_idx = 0
    path[0] = last_idx
    mask[last_idx] = False
    for k in range(1, n):
        last_idx = idx[mask][numpy.argmin(d[last_idx, mask])]
        path[k] = last_idx
        mask[last_idx] = False
        
    stop_timer = perf_counter_ns()
    runtime = stop_timer-start_timer
    
    return path, runtime


graph2 = numpy.random.rand(100,100)
graph1 = numpy.array([[1,20,30],[5,4,2],[3,2,2]])
print(nearest_neighbor(graph2))
#print(graph2)
