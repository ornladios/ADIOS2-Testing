from summit_node_layouts import summit_node_layouts
from create_sweep_groups import create_sweep_groups

# Parameters
writer_np               = [80]
reader_np               = [8]
engines                 = [ {'BP4':{'OpenTimeoutSecs':'30.0'}},
                            {'SST':{'DataTransport':'RDMA'}},
                            {"SSC":{}},
                            {"Null":{}}
                          ]
adios_xml_file          = 'copro.xml'
config_file             = ['copro-80.txt']
run_repetitions         = 1
batch_job_timeout_secs  = 600
per_experiment_timeout  = 100


node_layouts = summit_node_layouts('writer', 'reader')

sweep_groups = create_sweep_groups ('summit',
                                    writer_np,
                                    reader_np,
                                    engines,
                                    node_layouts,
                                    adios_xml_file,
                                    config_file,
                                    run_repetitions,
                                    batch_job_timeout_secs,
                                    per_experiment_timeout)


