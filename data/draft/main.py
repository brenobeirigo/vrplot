# %%

import vrplot.util as util
import vrplot.opt.complexity as complexity
import itertools
coords = util.get_random_nodes(6)

# Transformation to set exclude duplicate permutations
ways = set(itertools.permutations(("*","*","|")))


print(f"k={4} vehicles can pick up n={3} customers in {len(ways)} different ways.\n")
print("# Ways (vehicles are separated by '|'):")

complexity.enumerate_ways(ways)

# %%
