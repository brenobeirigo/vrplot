import vrplot.util as util
import numpy as np


def get_prob_acceptance(current_route_cost, candidate_route_cost, T):
    prob = np.exp(-(candidate_route_cost - current_route_cost)/T)
    #print(current_route_cost, candidate_route_cost, T, prob)
    return prob


def accept(current_route_cost, candidate_route_cost, T):
    if candidate_route_cost < current_route_cost:
        return True
    else:
        return np.random.rand() < get_prob_acceptance(current_route_cost, candidate_route_cost, T)


def simulated_annealing(
        starting_route,
        coords,
        initial_temperature=None,
        min_temp=0.01,
        cooling_factor=0.5,
        max_iterations_at_current_temp=1000):

    solution_cost_list = []

    current_route = list(starting_route)
    current_route_cost = util.get_cost(current_route, coords)

    # Current route is currently the best
    best_route = current_route
    best_route_cost = current_route_cost

    # Initial temperature
    if initial_temperature is None:
        T = current_route_cost*cooling_factor
    else:
        T = initial_temperature

    while True:
        
        # print(f"# T = {T:7.3f}"
        #       f"\n    Best: {best_route_cost:12,.3f} - Route: {best_route}"
        #       f"\n Current: {current_route_cost:12,.3f} - Route: {current_route}"
        #       )
        
        # Stopping criteria
        if T < min_temp:
            break
        
        iterations_at_T = 0

        while True:  # At a fixed temperature

            # Generate a candidate solution using random sub-tour reversal
            candidate_route = get_route_subtour_reversal(current_route)
            candidate_route_cost = util.get_cost(candidate_route, coords)

            if accept(current_route_cost, candidate_route_cost, T):

                # Save the best route so far
                if candidate_route_cost < best_route_cost:
                    best_route_cost = candidate_route_cost
                    best_route = candidate_route

                # print(f"{iterations_at_T:>8} "
                #       f"- Cost: {current_route_cost:10,.3f} "
                #       f"- Cost: {candidate_route_cost:10,.3f} "
                #       f"- Best: {best_route_cost:10,.3f} "
                #       f"-    T: {T:7.3f} "
                #       f" \nRoute1: {list(current_route)} = {util.get_cost(current_route, coords):12,.5f}"
                #       f" \nRoute2: {list(candidate_route)} = {util.get_cost(candidate_route, coords):12,.5f}"
                #       )
                current_route = candidate_route
                current_route_cost = candidate_route_cost

            solution_cost_list.append(current_route_cost)

            iterations_at_T += 1

            # Equilibrium condition (max number of iterations reached)
            if iterations_at_T >= max_iterations_at_current_temp:
                break


        # Temperature update
        T = cooling_factor*T

    return best_route, solution_cost_list


def get_route_subtour_reversal(route):

    new_route = np.array(route)

    ## Random subsequence (excluding depots)
    j = np.random.randint(2, len(route) - 1)

    # Prevent full reversal
    while j == len(route) - 2:
        j = np.random.randint(2, len(route) - 1)

    i = np.random.randint(1, len(route) - j)

    # Replace subsequence by its reversed order
    new_route[i: (i + j)] = route[i: (i + j)][::-1]

    return new_route


# np.random.seed(42)

# us_nodes, us_coords = static.get_data_us_capitals()
# us_depot, us_customer_nodes = us_nodes[0], us_nodes[1:]

# fa_us_route, _ = heuristic.get_route_farthest_addition(
#     us_customer_nodes,
#     us_coords,
#     start=np.random.randint(len(us_nodes)))

# improved_2opt_fa_us_route = heuristic.neighborhood_search_2opt(fa_us_route, us_coords)
# best_route, costs = simulated_annealing(improved_2opt_fa_us_route, us_coords)
# print(len(costs))