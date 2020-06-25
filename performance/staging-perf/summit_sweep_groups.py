from sweep_groups_helper import create_sweep_groups
from summit_node_layouts import summit_node_layouts


# Parameters
writer_np               = [128, 512, 2048, 8192]
reader_np_ratio         = [2,8]
writers_per_node_summit = [32]
size_per_pe             = ['1MB', '16MB', '512MB']
engines                 = ['bp4', 'sst-tcp', 'sst-rdma', 'ssc', 'insitumpi']
run_repetitions         = 2
batch_job_timeout_secs  = 3600
per_experiment_timeout  = 600


node_layouts = summit_node_layouts('writer', 'reader')

sweep_groups = create_sweep_groups ('summit',
                                    writer_np,
                                    reader_np_ratio,
                                    size_per_pe,
                                    engines,
                                    node_layouts,
                                    run_repetitions,
                                    batch_job_timeout_secs,
                                    per_experiment_timeout)

