from codar.savanna.machines import SummitNode


#----------------------------------------------------------------------------#
def summit_node_layouts(w):
    """
    Get the list of node layouts that you want to explore for Summit.
    Returns 2 node layouts:
        - separate nodes, with 32 writers and readers on each node
        - colocated, with 32 writers and 4 readers on each node
    Input args:
    w - Name of the writer application
    """

    nl = []
    nl.append( separate(32, w))
    nl.append( shared  (32, w))

    return nl


#----------------------------------------------------------------------------#
def shared(nw, wn):
    """
    Creates a shared node layout for Summit with nw writers/node.
    Spreads writer ranks evenly across the 2 sockets.

    Input args:
    nw = num writers
    wn = writer app name
    """

    n = SummitNode()
    for i in range(nw//2):
        n.cpu[i] = "{}:{}".format(wn, i)
    for i in range(nw//2):
        n.cpu[i+21] = "{}:{}".format(wn, i+nw//2)


    return [n]


#----------------------------------------------------------------------------#
def separate(nw, wn):
    """
    Create separate nodes on Summit for the writer processes.
    Spawns 32 writers on each node, 16 on each socket
    
    Input args:
    nw = num writers
    wn = writer app name
    """
    node_w = SummitNode()
    for i in range(nw//2):
        node_w.cpu[i] = "{}:{}".format(wn, i)
    for i in range(nw//2):
        node_w.cpu[i+21] = "{}:{}".format(wn, i+nw//2)

    return [node_w]

