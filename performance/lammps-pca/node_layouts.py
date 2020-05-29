from codar.savanna.machines import SummitNode

#----------------------------------------------------------------------------#
def all_sim_nodes():
    """
    Create a node layout where the simulation and the analysis ranks reside
    on separate nodes.
    """

    # Create a node layout for the simulation
    # Lets have 42 ranks consume all 42 cores on each summit node
    sim_node = SummitNode()
    for i in range(42):
        sim_node.cpu[i] = "sim_inline_rdf_calc:{}".format(i)

    # Return a list object
    return [sim_node]

#----------------------------------------------------------------------------#
def separate_nodes():
    """
    Create a node layout where the simulation and the analysis ranks reside
    on separate nodes.
    """

    # Create a node layout for the simulation
    # Lets have 42 ranks consume all 42 cores on each summit node
    sim_node = SummitNode()
    for i in range(42):
        sim_node.cpu[i] = "simulation:{}".format(i)

    # Create a node layout for the analysis.
    analysis_node = SummitNode()
    for i in range(42):
        analysis_node.cpu[i] = "rdf_calc:{}".format(i)

    # Return a list object
    return [sim_node, analysis_node]


#----------------------------------------------------------------------------#
def share_nodes_21to21():
    """
    Create a shared node layout where the simulation and analysis ranks share
    compute nodes
    """
    
    shared_node = SummitNode()
    for i in range(21):
        shared_node.cpu[i] = "simulation:{}".format(i)
        shared_node.cpu[21+i] = "rdf_calc:{}".format(i)

    return [shared_node]


#----------------------------------------------------------------------------#
def share_nodes_28to14():
    """
    Create a shared node layout where the simulation and analysis ranks share
    compute nodes
    """
    
    shared_node = SummitNode()
    for i in range(28):
        shared_node.cpu[i] = "simulation:{}".format(i)
    for i in range(14):
        shared_node.cpu[28+i] = "rdf_calc:{}".format(i)

    return [shared_node]

#----------------------------------------------------------------------------#
def share_nodes_35to7():
    """
    Create a shared node layout where the simulation and analysis ranks share
    compute nodes
    """
    
    shared_node = SummitNode()
    for i in range(35):
        shared_node.cpu[i] = "simulation:{}".format(i)
    for i in range(7):
        shared_node.cpu[35+i] = "rdf_calc:{}".format(i)

    return [shared_node]

#----------------------------------------------------------------------------#
def share_nodes_40to2():
    """
    Create a shared node layout where the simulation and analysis ranks share
    compute nodes
    """
    
    shared_node = SummitNode()
    for i in range(40):
        shared_node.cpu[i] = "simulation:{}".format(i)
    for i in range(2):
        shared_node.cpu[40+i] = "rdf_calc:{}".format(i)

    return [shared_node]

