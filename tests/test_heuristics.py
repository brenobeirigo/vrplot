from vrplot.opt.heuristic import get_route_2opt
from vrplot.opt.metaheuristic import simulated_annealing
from vrplot.util import get_random_nodes, get_cost
import numpy as np
np.random.seed(7)

def test_2opt():
    coords = get_random_nodes(6)
    
    route2opt = get_route_2opt((0,1,2,3,4,5,0), coords)
    print(route2opt)
    
    
print(test_2opt())

def test_sa():
    coords = get_random_nodes(50)
    nodes = list(range(len(coords)))

    route = tuple([nodes[0]] + nodes[1:] + [nodes[0]])
    best, costs = simulated_annealing(route, coords, min_temp=0.1, max_iterations_at_current_temp=100)
    print(best)
    # print(f"BEST:", get_cost(best, coords))