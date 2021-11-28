import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import util


def construct_route(route, nodes, coords, figsize=(5,5), hide_axis_labels=True):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(f"Cost: {util.get_cost(route, coords):6.2f}")
    draw_nodes(coords, nodes, ax)
    draw_route(route, coords, ax)
    
    if hide_axis_labels:
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])
        
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

def draw_nodes(coords, node_labels, ax, hide_axis_labels=True):
    # Set limit box
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

def draw_routes(routes, node_ids, coords, vehicle_route_colors, ax, hide_axis_labels=True):

    # Erase previous graph
    ax.cla()
    
    # Set limit box
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    
    # Print total cost (sum of all route costs)
    ax.set_title(f"Cost: {util.get_total_cost(routes, coords):6.2f}")
    
    # Draw routes and points
    draw_vehicle_routes(routes, vehicle_route_colors, coords, ax)
    draw_points(coords, node_ids, ax)        
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, frameon=False)
    
    if hide_axis_labels:
        ax.axes.xaxis.set_ticklabels([])
        ax.axes.yaxis.set_ticklabels([])