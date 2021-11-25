import matplotlib.patches as patches
import numpy as np
np.random.seed(42)


################################################################################
## COST ########################################################################
################################################################################

def euclidean_dist(v1, v2):
    return np.sqrt(np.sum((np.array(v1) - np.array(v2)) ** 2))   

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

def get_random_solution(n_customers, n_vehicles):
    routes = []
    customer_ids = np.arange(1,n_customers+1)
    for _ in range(n_vehicles-1):
        
        if len(customer_ids) == 1:
            break
        
        size = np.random.randint(low=1, high=len(customer_ids))
        route = list(np.random.choice(customer_ids, size=size, replace=False))
        routes.append(tuple(route))
        customer_ids = list(set(customer_ids).difference(route))
    
    if len(customer_ids) > 0:
        np.random.shuffle(customer_ids)
        routes.append(tuple(customer_ids))
    return tuple(routes)
 
def get_greedy_route(nodes, node_coords, depot=0):

    nodes_to_visit = list(nodes)
    route = [depot]

    while len(nodes_to_visit) > 0:
        
        last_visited_coord = node_coords[route[-1]]
        
        # List of cost distances to visit all the other nodes departing from
        # the last visited node
        costs = [
            euclidean_dist(last_visited_coord, node_coords[candidate_node])
            for candidate_node in nodes_to_visit]
        
        closest_node_pos = np.argmin(costs)
        next_visit = nodes_to_visit[closest_node_pos]

        # Add closest node to route
        route.append(next_visit)

        # Update list of nodes to visit
        del nodes_to_visit[closest_node_pos]

        # Update the last visited node
        last_visited_node = next_visit

    route.append(depot)
    return tuple(route)
 
################################################################################
## PLOT ########################################################################
################################################################################

def draw_edge(od, coords, ax, color="k"):
    o, d = od
    o_x, o_y = coords[o]
    d_x, d_y = coords[d]
    edge = patches.FancyArrowPatch(
                (o_x, o_y),
                (d_x, d_y),
                edgecolor=color,
                arrowstyle='->',
                linewidth=1,
                mutation_scale=10,
                connectionstyle="arc", # angle = manhattan connection
                zorder=0)
    ax.add_artist(edge)


def draw_route(route, coords, ax, color="k"):
    for od in zip(route[:-1], route[1:]):
        draw_edge(od, coords, ax, color="red")


def draw_points(coords, node_ids, ax):
    x,y = zip(*coords)
    x_depot, y_depot = x[0], y[0]
    x_customers, y_customers = x[1:],y[1:]
    ax.scatter(x_customers, y_customers, color="k", s=5, label="Customers")
    ax.scatter([x_depot], [y_depot], color="k", marker='s', s=20, label="Depot")
    draw_labels(node_ids, coords, ax)

def init_plot(coords ,node_ids, ax):
    # Set limit box
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    draw_points(coords, node_ids, ax)        
    ax.legend()

def draw_vehicle_routes(routes, route_colors, coords, ax):
    for route, color in zip(routes, route_colors):
        draw_route([0] + list(route) + [0], coords, ax, color=color)


def draw_labels(node_labels, node_coords, ax):
    for n, label in enumerate(node_labels):
        ax.annotate(
            str(label),
            xy=node_coords[n],
            xytext=(-4, 6),
            textcoords="offset points")

def draw_routes(routes, node_ids, coords, vehicle_route_colors, ax):

    # Erase previous graph
    ax.cla()
    
    # Set limit box
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    
    # Print total cost (sum of all route costs)
    ax.set_title(f"Cost: {get_total_cost(routes, coords):6.2f}")
    
    # Draw routes and points
    draw_vehicle_routes(routes, vehicle_route_colors, coords, ax)
    draw_points(coords, node_ids, ax)        
    
    ax.legend()
