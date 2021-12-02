import itertools
import numpy as np


def get_ways_to_split_nitems_to_kbins(
    nitems, kbins, item_separator="┃", item_symbol="🧍"
):

    items = [item_symbol] * nitems

    # E.g., 3 bins = 2item separators
    separators = [item_separator] * (kbins - 1)

    symbols = items + separators
    ways = set(itertools.permutations(symbols))
    return ways


def get_ways_to_split_list_in_kbins(
    items, kbins, item_separator="┃", item_symbol="🧍"
):

    separation_ways = get_ways_to_split_nitems_to_kbins(
        len(items),
        kbins,
        item_separator=item_separator,
        item_symbol=item_symbol,
    )

    ways_pos_separators = [
        [i for i in range(len(w)) if w[i] == item_separator]
        for w in separation_ways
    ]

    ways = []
    for pos_separators in ways_pos_separators:
        aux = list(items)
        for p in pos_separators:
            aux.insert(p, item_separator)
        ways.append(aux)

    return ways


def enumerate_ways(ways):
    for i, way in enumerate(sorted(["".join(map(str, w)) for w in ways])):
        print(f"{i+1:>3}  {way}")


def get_solution_space(
    customers, depot=0, n_vehicles=1, distinguish_vehicles=True
):

    item_sep = "|"

    # Only accept single-digit customer ids
    if np.max(customers) > 9:
        return None

    routes = set()

    if n_vehicles > 1:

        symbol_permutations = itertools.permutations(
            [item_sep] * (n_vehicles - 1) + customers
        )

        for s in symbol_permutations:
            fleet_routes = ()
            i = 0
            for j, p in enumerate(s):
                if p == item_sep:
                    if i == j:
                        vehicle_route = (depot,) + (depot,)
                    else:
                        vehicle_route = (depot,) + s[i:j] + (depot,)
                    i = j + 1

                    fleet_routes += (vehicle_route,)

            ## Add last vehicle route
            vehicle_route = (depot,) + s[i:] + (depot,)
            fleet_routes += (vehicle_route,)

            routes.add(tuple(fleet_routes))

        if not distinguish_vehicles:
            routes = set([(tuple(sorted(r))) for r in routes])
    else:
        routes = {
            ((depot,) + tuple(p) + (depot,),)
            for p in itertools.permutations(customers)
        }

    return routes
