from codar.savanna.machines import SummitNode


def shared(nw, nr, wn, rn):
    """
    Creates a shared node layout for Summit with nw writers/node and nr readers/node.
    Spreads writer and reader ranks evenly across the 2 sockets.

    Input args:
    nw = num writers
    nr = num readers
    wn = writer app name
    rn = reader app name
    """

    n = SummitNode()
    for i in range(nw//2):
        n.cpu[i] = "{}:{}".format(wn, i)
    for i in range(nw//2):
        n.cpu[i+21] = "{}:{}".format(wn, i+nw//2)

    for i in range(nr//2):
        n.cpu[i+nw//2] = "{}:{}".format(rn, i)
    for i in range(nr//2):
        n.cpu[i+nw//2+21] = "{}:{}".format(rn, i+nr//2)

    return [n]


def separate(nw, nr, wn, rn):
    """
    Create separate nodes on Summit for the writer and reader processes.
    Spawns 32 writers/readers on each node, 16 on each socket
    
    Input args:
    nw = num writers
    nr = num readers
    wn = writer app name
    rn = reader app name
    """
    node_w = SummitNode()
    for i in range(nw//2):
        node_w.cpu[i] = "{}:{}".format(wn, i)
    for i in range(nw//2):
        node_w.cpu[i+21] = "{}:{}".format(wn, i+nw//2)

    node_r = SummitNode()
    for i in range(nr//2):
        node_r.cpu[i] = "{}:{}".format(rn, i)
    for i in range(nr//2):
        node_r.cpu[i+21] = "{}:{}".format(rn, i+nr//2)

    return [node_w, node_r]

