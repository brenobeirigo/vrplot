################################################################################
## PLOT ########################################################################
################################################################################

# ANIMATIONS
#%matplotlib widget
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
from vrplot import util, static


def show_solutions(solutions, coords, node_labels, fig=None, ax=None, figsize=(8,8), vehicle_route_colors = ['#e41a1c', '#377eb8','#4daf4a','#984ea3','#ff7f00', '#ffff33']):
    if ax == None or fig==None:
        figure, axis = plt.subplots(figsize=figsize)
        axis.set_xlim(0,1)
        axis.set_ylim(0,1)
        lim = 0,1,0,1
    else:
        lim = None
        figure, axis = fig, ax

    animator = animation.FuncAnimation(
        figure,
        static.draw_routes,
        solutions,
        fargs=(coords, node_labels, vehicle_route_colors, axis,lim),
        interval=100,
        repeat=False)
    plt.close()
    return HTML(animator.to_html5_video())


def construct_route(route, coords, node_labels, fig=None, ax=None, figsize=(8,8), route_color="red"):
    
    if ax == None or fig==None:
        figure, axis = plt.subplots(figsize=figsize)
        axis.set_xlim(0,1)
        axis.set_ylim(0,1)
    else:
        figure, axis = fig, ax
        
    static.draw_nodes(coords, node_labels, axis)        
    axis.set_title(static.cost_header(util.get_cost(route, coords)))

    edges = list(zip(route[:-1], route[1:]))

    animator = animation.FuncAnimation(
        figure,
        static.draw_edge,
        edges,
        fargs=(coords, axis, route_color),
        interval=100,
        repeat=False)
    
    plt.close()
    return HTML(animator.to_html5_video())

    # If not closed, plot the first solution
    #plt.close()
    #return HTML(animator.to_html5_video())
  
