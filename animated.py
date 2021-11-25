################################################################################
## PLOT ########################################################################
################################################################################

# ANIMATIONS
#%matplotlib widget
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
import static
import util


def show_solutions(solutions, node_coords, node_ids, figsize=(8,8), vehicle_route_colors = ['#e41a1c', '#377eb8','#4daf4a','#984ea3','#ff7f00', '#ffff33']):
    fig, ax = plt.subplots(figsize=figsize)

    animator = animation.FuncAnimation(
        fig,
        static.draw_routes,
        solutions,
        fargs=(node_ids, node_coords, vehicle_route_colors, ax,),
        interval=100,
        repeat=False)
    plt.close()
    return HTML(animator.to_html5_video())


def construct_route(route, node_coords, node_ids, figsize=(8,8), route_color="red"):
    fig, ax = plt.subplots(figsize=figsize)
    static.draw_nodes(node_coords, node_ids, ax)        
    ax.set_title(f"Cost: {util.get_cost(route, node_coords):6.2f}")

    edges = list(zip(route[:-1], route[1:]))

    animator = animation.FuncAnimation(
        fig,
        static.draw_edge,
        edges,
        fargs=(node_coords, ax, route_color),
        interval=100,
        repeat=False)
    
    plt.close()
    return HTML(animator.to_html5_video())

    # If not closed, plot the first solution
    #plt.close()
    #return HTML(animator.to_html5_video())
  
