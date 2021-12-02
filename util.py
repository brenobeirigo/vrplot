import numpy as np

def get_random_nodes(n_customers, x_depot=0.5, y_depot=0.5):
    # Random x and y coordinates for customers
    x_customers = np.random.rand(n_customers)
    y_customers = np.random.rand(n_customers)

    # List of coordinates with depot at the beginning
    node_coords = [(x_depot, y_depot)] + list(zip(x_customers, y_customers))
    
    return node_coords

################################################################################
## COST ########################################################################
################################################################################

def euclidean_dist(v1, v2):
    return np.sqrt(np.sum((np.array(v1) - np.array(v2)) ** 2))   

def dist(i,j, coords):
    return euclidean_dist(coords[i], coords[j])

def get_cost(route, coords):
    cost = 0
    for o,d in zip(route[1:], route[:-1]):
        cost+=euclidean_dist(coords[o], coords[d])
    return cost

def get_total_cost(routes, coords):
    total_cost = 0
    for route in routes:
        total_cost+=get_cost(route, coords)
    return total_cost
  
################################################################################
## SOLUTION STRATEGIES #########################################################
################################################################################

def get_best_permutation(customer_ids, n_vehicles=1, depot=0):
    routes = []
    for _ in range(n_vehicles-1):
        
        if len(customer_ids) == 1:
            break
        
        size = np.random.randint(low=1, high=len(customer_ids))
        route = list(np.random.choice(customer_ids, size=size, replace=False))
        routes.append((depot,) +tuple(route) + (depot,))
        customer_ids = list(set(customer_ids).difference(route))
    
    if len(customer_ids) > 0:
        np.random.shuffle(customer_ids)
        
        routes.append((depot,) + tuple(customer_ids) + (depot,))
    return tuple(routes)

def get_random_solution(customer_ids, n_vehicles=1, depot=0):
    routes = []
    for _ in range(n_vehicles-1):
        
        if len(customer_ids) == 1:
            break
        
        size = np.random.randint(low=1, high=len(customer_ids))
        route = list(np.random.choice(customer_ids, size=size, replace=False))
        routes.append((depot,) +tuple(route) + (depot,))
        customer_ids = list(set(customer_ids).difference(route))
    
    if len(customer_ids) > 0:
        np.random.shuffle(customer_ids)
        
        routes.append((depot,) + tuple(customer_ids) + (depot,))
    return tuple(routes)
