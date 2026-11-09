import math
from vrplot import util


def test_euclidean_dist():
    v1 = (0, 0)
    v2 = (3, 4)
    assert util.euclidean_dist(v1, v2) == 5.0


def test_get_cost_and_total_cost():
    coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
    route = (0, 1, 2, 3, 0)
    cost = util.get_cost(route, coords)
    # square perimeter
    assert math.isclose(cost, 4.0, rel_tol=1e-9)

    routes = (route,)
    assert math.isclose(util.get_total_cost(routes, coords), 4.0, rel_tol=1e-9)


def test_get_random_nodes_basic_properties():
    nodes = util.get_random_nodes(5)
    # should include depot + 5 customers
    assert len(nodes) == 6
    # depot should be first and equal to default (0.5,0.5)
    assert nodes[0] == (0.5, 0.5)
