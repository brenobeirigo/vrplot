from collections import deque
from vrplot.util import euclidean_dist, dist, get_cost
import numpy as np
import itertools
from copy import copy


def get_route_nearest_neighborhood(nodes, node_coords, start=0, depot=0):

    nodes_to_visit = [depot] + list(nodes)
    route = deque([start])
    
    nodes_to_visit.remove(start)

    while len(nodes_to_visit) > 0:
        
        last_visited_coord = node_coords[route[-1]]
        
        # List of cost distances to visit all the other nodes departing from
        # the last visited node
        closest_node_cost = np.inf
        next_visit_pos = None
        for pos, candidate_node in enumerate(nodes_to_visit):
            cost = euclidean_dist(last_visited_coord, node_coords[candidate_node])
            if cost < closest_node_cost:
                closest_node_cost = cost
                next_visit_pos = pos
        
        next_visit = nodes_to_visit[next_visit_pos]

        # Add closest node to route
        route.append(next_visit)

        # Update list of nodes to visit
        del nodes_to_visit[next_visit_pos]

    # Put depot in the beginning
    route.rotate(len(route)-route.index(depot))
    route.append(depot)
    return tuple(route)

def get_farthest_node_pos(n, nodes_to_visit, node_coords):
    last_visited_coord = node_coords[n]
    
    farthest_node_pos = None
    farthest_node_cost = -1
    for i, candidate_node in enumerate(nodes_to_visit):
        cost = euclidean_dist(last_visited_coord, node_coords[candidate_node])
        if cost > farthest_node_cost:
            farthest_node_pos, farthest_node_cost = i, cost
    
    return farthest_node_pos, farthest_node_cost

def cheapest_insertion_pos(n, route, node_coords):
    
    if len(route) == 1:
        return 1
    
    cheapest_insertion_cost = np.inf
    insertion_pos = None

    coord_n = node_coords[n]
    for i in range(len(route)-1):
        o, d = route[i], route[i+1]
        coord_o, coord_d = node_coords[o], node_coords[d]
        n_insertion_cost = (euclidean_dist(coord_o, coord_n)
                +  euclidean_dist(coord_n, coord_d)
                -  euclidean_dist(coord_o, coord_d))
        if n_insertion_cost < cheapest_insertion_cost:
            cheapest_insertion_cost = n_insertion_cost
            insertion_pos = i + 1
    return insertion_pos

def get_route_farthest_addition(nodes, node_coords, start=0, depot=0):

    nodes_to_visit = [depot] + list(nodes)
    route = deque([start])
    sols = []
    nodes_to_visit.remove(start)
    
    
    while len(nodes_to_visit) > 0:
        
        farthest_node_pos = None
        farthest_node_cost = -1
        
        for n in route:
            
            n_farthest_node_pos, n_cost = get_farthest_node_pos(n, nodes_to_visit, node_coords)

            if n_cost > farthest_node_cost:
                farthest_node_pos, farthest_node_cost = n_farthest_node_pos, n_cost

        # Add farthest node to route
        next_visit = nodes_to_visit[farthest_node_pos]
        j = cheapest_insertion_pos(next_visit, route, node_coords)
        route.insert(j, next_visit)
        sols.append(copy(route))

        # Update list of nodes to visit
        del nodes_to_visit[farthest_node_pos]

    
    route.rotate(len(route)-route.index(depot))
    
    # Last connection of farthest addition process
    last_sol = copy(sols[-1])
    last_sol.append(start)
    sols.append(last_sol)
    route.append(depot)
    
    return tuple(route), [(tuple(s),) for s in sols]

def get_route_2opt(route, coords):
    
    min_change = 0
    # Find the best move
    for i in range(len(route) - 2):
        for j in range(i + 2, len(route) - 1):
            
            # Symmetric distances -> change only the tour length between 4 cities
            change = (
                dist(route[i], route[j], coords)
                + dist(route[i+1], route[j+1], coords)
                - dist(route[i], route[i+1], coords)
                - dist(route[j], route[j+1], coords))
            if change < min_change:
                min_change = change
                min_i, min_j = i, j
    
    # Update route with best move
    route_updated = np.array(route)
    if min_change < 0:
        route_updated[min_i+1:min_j+1] = route_updated[min_i+1:min_j+1][::-1]
    
    return tuple(route_updated)

def neighborhood_search_2opt(route, coords, stop_after=None):
    
    route_cost = get_cost(route, coords)

    improvement_history = [(route, route_cost)]

    while True:
        
        if stop_after !=None and len(improvement_history) >= stop_after:
            break
        
        improved_route = get_route_2opt(route, coords)
        improved_route_cost = get_cost(improved_route, coords)
        
        if improved_route_cost < route_cost:
            improvement_history.append((improved_route, improved_route_cost))    
            route = improved_route
            route_cost = improved_route_cost
 
        else:
            break
    
    return route, improvement_history

    