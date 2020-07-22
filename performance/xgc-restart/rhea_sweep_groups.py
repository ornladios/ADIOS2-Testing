from codar.savanna.machines import SummitNode
from sweep_groups_helper import create_sweep_groups
from summit_node_layouts import summit_node_layouts
# Parameters 64, 256, 1024 nodes  16 processes per node
writer_np               = [1024, 4096, 16384]
reader_np_ratio         = [1]
writers_per_node        = [16]
size_per_pe             = []
engines                 = ['bp4']
run_repetitions         = 0
batch_job_timeout_secs  = 3600
per_experiment_timeout  = 600

node_layouts = list()
node_layouts.append([{'writer':16}, {'reader': 16}])
n = SummitNode()
for i in range(writers_per_node):
    n.cpu[i] = "{}:{}".format("writer", i)
    n.cpu[i + writers_per_node] = "{}:{}".format("reader", i)
node_layouts = list(n)
sweep_groups = create_sweep_groups ('rhea',
                                    writer_np,
                                    reader_np_ratio,
                                    size_per_pe,
                                    engines,
                                    node_layouts,
                                    run_repetitions,
                                    batch_job_timeout_secs,
                                    per_experiment_timeout)