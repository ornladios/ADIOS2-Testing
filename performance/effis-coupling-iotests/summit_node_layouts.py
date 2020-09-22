from codar.savanna.machines import SummitNode


#----------------------------------------------------------------------------#
def summit_node_layouts(x, g, c):
    """
    Get the list of node layouts that you want to explore for Summit.
    Returns 2 node layouts:
        - separate nodes, with 32 writers and readers on each node
        - colocated, with 32 writers and 4 readers on each node
    Input args:
    w - Name of the writer application
    r - Name of the reader application
    """

    nl = []
    nl.append( separate(42, 42, 42, x, g, c))

    return nl


#----------------------------------------------------------------------------#
def separate(nx, ng, nc, x, g, c):

    node_x = SummitNode()
    for i in range(nx//2):
        node_x.cpu[i] = "{}:{}".format(x, i)
    for i in range(nx//2):
        node_x.cpu[i+21] = "{}:{}".format(x, i+nx//2)

    node_g = SummitNode()
    for i in range(ng//2):
        node_g.cpu[i] = "{}:{}".format(g, i)
    for i in range(ng//2):
        node_g.cpu[i+21] = "{}:{}".format(g, i+ng//2)

    node_c = SummitNode()
    for i in range(nc//2):
        node_c.cpu[i] = "{}:{}".format(c, i)
    for i in range(nc//2):
        node_c.cpu[i+21] = "{}:{}".format(c, i+nc//2)

    return [node_x, node_g, node_c]

