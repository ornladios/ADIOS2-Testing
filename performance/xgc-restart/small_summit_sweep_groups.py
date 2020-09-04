from codar.savanna.machines import SummitNode
from sweep_groups_helper import create_sweep_groups

# Parameters 16 nodes for a night run
writer_np               = [96]
reader_np_ratio         = [1]
writers_per_node_summit = [6]
size_per_pe             = []
engines                 = ['bp4']
run_repetitions         = 4
batch_job_timeout_secs  = 3600
per_experiment_timeout  = 600

n = SummitNode()
for i in range(writers_per_node_summit[0]):
   n.cpu[i] = "{}:{}".format("writer", i)
   n.cpu[i + writers_per_node_summit[0]] = "{}:{}".format("reader", i)

node_layouts = [[n]]

sweep_groups = create_sweep_groups ('smallsummit',
                                    writer_np,
                                    reader_np_ratio,
                                    size_per_pe,
                                    engines,
                                    node_layouts,
                                    run_repetitions,
                                    batch_job_timeout_secs,
                                    per_experiment_timeout)

