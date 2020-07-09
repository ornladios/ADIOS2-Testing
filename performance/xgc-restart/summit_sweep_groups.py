from sweep_groups_helper import create_sweep_groups
from summit_node_layouts import summit_node_layouts


# Parameters
writer_np               = [48]
reader_np_ratio         = [1]
writers_per_node_summit = [6]
size_per_pe             = []
engines                 = ['bp4']
run_repetitions         = 1
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

