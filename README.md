# VRPlot

Plot vehicle routing problem (VRP) routes

## Installation

Install core runtime requirements (recommended in a virtualenv):

```bash
pip install -e .
pip install numpy matplotlib
```

Optional extras (exact MIP solver) are available separately; Gurobi must be installed per vendor instructions:

```bash
pip install -e .[mip]
```

## Quickstart

Minimal example generating random nodes, building a simple route and plotting it:

```python
from vrplot import util, static

# generate 8 random customers (depot at index 0)
coords = util.get_random_nodes(8)
node_labels = list(range(len(coords)))

# simple route visiting nodes in order and returning to depot (0)
route = tuple(range(len(coords))) + (0,)

fig, ax = static.construct_route(route, coords, node_labels)
fig.show()
```

## Notes

- Core dependencies: `numpy`, `matplotlib`.
- Optional solver: `gurobipy` (not installed via PyPI without Gurobi license).
- Examples and demos are available in the `notebooks/` folder.

Contributions and issues are welcome.
