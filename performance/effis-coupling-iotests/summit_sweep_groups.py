from sweep_groups_helper import create_sweep_groups
from summit_node_layouts import summit_node_layouts


# Parameters
x_np                    = [1024]
g_np                    = [128]
c_np                    = [128]
engines                 = ['bp4', 'insitumpi', 'sst-tcp', 'sst-rdma', 'ssc']
run_repetitions         = 0
batch_job_timeout_secs  = 3600
per_experiment_timeout  = 600


node_layouts = summit_node_layouts('x', 'g', 'c')

sweep_groups = create_sweep_groups ('summit',
                                    x_np,
                                    g_np,
                                    c_np,
                                    engines,
                                    node_layouts,
                                    run_repetitions,
                                    batch_job_timeout_secs,
                                    per_experiment_timeout)

