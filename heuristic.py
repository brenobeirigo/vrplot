from collections import deque
from util import euclidean_dist
import numpy as np
import static, util
import itertools
from copy import copy


def get_possible_schedules(*vehicle_customer_assignments):
    schedules = []
    for vehicle_customers in vehicle_customer_assignments:
        schedules.append(itertools.permutations(vehicle_customers))
    
    schedules = itertools.product(*schedules)
    return list(schedules)

def get_brute_force(customers, depot=0, n_vehicles=1, distinguish_vehicles=True):
    # Only accept single-digit customer ids
    if np.max(customers) > 9:
        return None
    
    routes = set(["".join(c) for c in list(itertools.permutations(["|"] *(n_vehicles-1) + list(map(str,set(customers)))))])
    routes = [tuple([(depot,)+tuple(map(int,list(e)))+(depot,) if e!="" else tuple([]) for e in r.split("|")]) for r in routes]
    
    if not distinguish_vehicles:
        routes = [tuple(r) for r in set([frozenset(r) for r in routes])]
    
    return routes


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

    # Put depot in the beginning
    route.rotate(len(route)-route.index(depot))
    route.append(depot)
    return tuple(route), [(tuple(s),) for s in sols]