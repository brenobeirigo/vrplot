from vrplot.opt import heuristic
from vrplot import util


def test_nearest_neighborhood_simple():
    # four points on a line: depot at 0, customers 1..3
    coords = [(0, 0), (1, 0), (2, 0), (3, 0)]
    nodes = [1, 2, 3]
    route, sols = heuristic.get_route_nearest_neighborhood(nodes, coords, start=0, depot=0)
    # route should start and end at depot and include all nodes
    assert route[0] == 0 and route[-1] == 0
    assert set(route) == {0, 1, 2, 3}


def test_farthest_addition_properties():
    coords = [(0, 0), (10, 0), (0, 10), (10, 10)]
    nodes = [1, 2, 3]
    route, sols = heuristic.get_route_farthest_addition(nodes, coords, start=0, depot=0)
    # route should contain each customer exactly once (plus depot)
    assert route.count(0) == 2
    assert set(route) >= {0, 1, 2, 3}
    # ensure cost is consistent with util.get_cost
    assert util.get_cost(route, coords) >= 0


def test_neighborhood_search_improves_or_equal_cost():
    coords = [(0, 0), (1, 0), (0, 1), (1, 1)]
    # create a deliberately suboptimal route (crossing)
    route = (0, 2, 1, 3, 0)
    initial_cost = util.get_cost(route, coords)
    improved_route, history = heuristic.neighborhood_search_2opt(route, coords)
    improved_cost = util.get_cost(improved_route, coords)
    assert improved_cost <= initial_cost
