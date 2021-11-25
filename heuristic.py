from collections import deque
from util import euclidean_dist
import numpy as np

def get_route_nearest_neighborhood(nodes, node_coords, start=0, depot=0):

    nodes_to_visit = [depot] + list(nodes)
    route = deque([start])
    
    nodes_to_visit.remove(start)

    while len(nodes_to_visit) > 0:
        
        last_visited_coord = node_coords[route[-1]]
        
        # List of cost distances to visit all the other nodes departing from
        # the last visited node
        costs = [
            euclidean_dist(last_visited_coord, node_coords[candidate_node])
            for candidate_node in nodes_to_visit]
        
        closest_node_pos = np.argmin(costs)
        next_visit = nodes_to_visit[closest_node_pos]

        # Add closest node to route
        route.append(next_visit)

        # Update list of nodes to visit
        del nodes_to_visit[closest_node_pos]

        # Update the last visited node
        last_visited_node = next_visit
    

    route.rotate(len(route)-route.index(depot))
    route.append(depot)
    return tuple(route)