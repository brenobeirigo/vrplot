import gurobipy as gp
from gurobipy import GRB
import math
from itertools import combinations
import vrplot

# SOURCE: https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/traveling_salesman/tsp_gcl.ipynb#scrollTo=qkCBabLarfBi

env = gp.Env(empty=True)
env.setParam('OutputFlag', 0)
env.start()


def get_solution_tsp(coords, nodes):

    # Callback - use lazy constraints to eliminate sub-tours

    def subtourelim(model, where):
        if where == GRB.Callback.MIPSOL:
            # make a list of edges selected in the solution
            vals = model.cbGetSolution(model._vars)
            selected = gp.tuplelist((i, j) for i, j in model._vars.keys()
                                if vals[i, j] > 0.5)
            # find the shortest cycle in the selected edge list
            tour = subtour(selected)
            if len(tour) < len(nodes):
                # add subtour elimination constr. for every pair of cities in subtour
                model.cbLazy(gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2))
                            <= len(tour)-1)

    # Given a tuplelist of edges, find the shortest subtour

    def subtour(edges):
        unvisited = list(nodes)
        cycle = list(nodes) # Dummy - guaranteed to be replaced
        while len(unvisited) > 0:  # true if list is non-empty
            thiscycle = []
            neighbors = unvisited
            while len(neighbors) > 0:
                current = neighbors[0]
                thiscycle.append(current)
                unvisited.remove(current)
                neighbors = [j for i, j in edges.select(current, '*')
                            if j in unvisited]
            if len(thiscycle) <= len(cycle):
                cycle = thiscycle # New shortest subtour
        return cycle
        
    # Compute pairwise distance matrix
    dist = {(c1, c2): vrplot.util.dist(c1, c2, coords) for c1, c2 in combinations(nodes, 2)}

    m = gp.Model()

    # Variables: is city 'i' adjacent to city 'j' on the tour?
    vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='x')

    # Symmetric direction: Copy the object
    for i, j in list(vars.keys()):
        vars[j, i] = vars[i, j]  # edge in opposite direction

    # Constraints: two edges incident to each city
    cons = m.addConstrs(vars.sum(c, '*') == 2 for c in nodes)

    m._vars = vars
    m.Params.lazyConstraints = 1

    m.optimize(subtourelim)

    # Retrieve solution
    vals = m.getAttr('x', vars)
    selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)

    tour = subtour(selected)
    return list(tour) + [nodes[0]], m.ObjVal