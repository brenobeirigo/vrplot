import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from vrplot import util

def get_data_us_capitals():
    # http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/index.html
    x_array = []
    y_array = []
    path_data = os.path.join(os.getcwd(), "vrplot", "data","att48.tsp")
    with open(path_data, "r") as f:
        
        for line in f.readlines()[6:-1]:
            _, x, y = line.split()
            x_array.append(int(x))
            y_array.append(int(y))

    coords = list(zip(x_array, y_array))
    return np.arange(len(x_array)), coords

def get_us_plot(figsize=(15,10), pad=500):
    us_nodes, us_coords = get_data_us_capitals()
    us_nodes = list(range(len(us_coords)))
    us_depot, us_customer_nodes = us_nodes[0], us_nodes[1:]

    us_fig, us_ax = plt.subplots(figsize=figsize)
    x, y = (list(zip(*us_coords)))
    us_ax.set_xlim(min(x)-pad, max(x)+pad)
    us_ax.set_ylim(min(y)-pad, max(y)+pad)
    return us_fig, us_ax

def construct_route(route, nodes, coords, fig=None, ax=None, figsize=(5,5), hide_axis_labels=True, label=None):
    if ax == None or fig == None:
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
    
    title = cost_header(util.get_cost(route, coords))
    
    if label != None:
        title = f"{label} ({title})"
        
    ax.set_title(title)
    draw_nodes(coords, nodes, ax)
    draw_route(route, coords, ax)
    
    if hide_axis_labels:
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
    
    return fig, ax
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


def draw_route(route, coords, ax, color="red"):
    for od in zip(route[:-1], route[1:]):
        draw_edge(od, coords, ax, color=color)


def draw_points(coords, node_labels, ax, show_labels=True):
    x,y = zip(*coords)
    x_depot, y_depot = x[0], y[0]
    x_customers, y_customers = x[1:],y[1:]
    ax.scatter(x_customers, y_customers, color="k", s=20, facecolors='none', edgecolors='k', label="Customers")
    ax.scatter([x_depot], [y_depot], color="k", marker='s', s=50, facecolors='gray', label="Depot")
    if show_labels:
        draw_labels(node_labels, coords, ax)

def draw_nodes(coords, node_labels, ax=None, figsize = (8, 8), hide_axis_labels=True):
    if ax == None:
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)

    draw_points(coords, node_labels, ax)        
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, frameon=False)
    
    if hide_axis_labels:
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])

def draw_vehicle_routes(routes, route_colors, coords, ax):
    for route, color in zip(routes, route_colors):
        draw_route(route, coords, ax, color=color)


def draw_labels(node_labels, node_coords, ax):
    for n, label in enumerate(node_labels):
        ax.annotate(
            str(label),
            xy=node_coords[n],
            xytext=(-4, 6),
            textcoords="offset points")

def draw_routes(routes, node_ids, coords, vehicle_route_colors, ax, lim=None, hide_axis_labels=True):

    # Erase previous graph
    ax.cla()
    
    # Set limit box
    if lim != None:
        xmin, xmax, ymin, ymax = lim
        ax.set_xlim(xmin,xmax)
        ax.set_ylim(xmin,xmax)
    
    # Print total cost (sum of all route costs)
    ax.set_title(cost_header(util.get_total_cost(routes, coords)))
    
    # Draw routes and points
    draw_vehicle_routes(routes, vehicle_route_colors, coords, ax)
    draw_points(coords, node_ids, ax)        
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, frameon=False)
    
    if hide_axis_labels:
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])

def cost_header(cost):
    return f"Cost: {cost:10,.2f}"