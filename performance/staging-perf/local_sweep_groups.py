from sweeps import create_experiment
from node_layouts import shared, separate
from codar.cheetah.parameters import SweepGroup


input_files = [
    'staging-perf-test-16MB-2to1.txt',
    'staging-perf-test-16MB-8to1.txt',
    'staging-perf-test-1MB-2to1.txt',
    'staging-perf-test-1MB-8to1.txt',
    'staging-perf-test-512MB-2to1.txt',
    'staging-perf-test-512MB-8to1.txt',
    'staging-perf-test-bp4.xml',
    'staging-perf-test-insitumpi.xml',
    'staging-perf-test-ssc.xml',
    'staging-perf-test-sst-rdma.xml',
    'staging-perf-test-sst-tcp.xml'
]


# Parameters
writer_np               = [1,2,4,8]
reader_np_ratio         = [2]
size_per_pe             = ['1MB', '16MB']
engines                 = ['bp4', 'insitumpi']
run_repetitions         = 2
batch_job_timeout_secs  = 3600
per_experiment_timeout  = 600


def create_sweep_groups():
    """
    Create sweep groups for this campaign
    """

    sweep_groups = []

    # sweep over writer processes 
    for n in writer_np:
        for e in engines:
            # Create a separate sweep group (batch job) for different values of writer nprocs
            sg = SweepGroup(
                    name                = "{}-processes-{}".format(n,e),
                    walltime            = batch_job_timeout_secs,
                    per_run_timeout     = per_experiment_timeout,
                    component_inputs    = {'writer': input_files},
                    run_repetitions     = run_repetitions,
                    parameter_groups    = None
                    )

            # Set launch mode to mpmd for insitumpi runs
            if 'insitumpi' in e: sg.launch_mode = 'mpmd'

            # Now lets create and add a list of sweep objects to this sweep group
            sweep_objs = []

            # Sweep over data size per process, engines, and the readers_ratio
            for s in size_per_pe:
                for r_ratio in reader_np_ratio:
        
                    # no. of reader ranks == no. of writers / reader_ratio
                    r = n//r_ratio
                    
                    config_fname = "staging-perf-test-{}-{}to1.txt".format(s,r)
                    scaling = '-w'
                    adios_xml = 'staging-perf-test-{}.xml'.format(e)
                    post_hoc = True if 'bp4' in e else False


                    # create a parameter sweep object for this parameter combination
                    sweep_obj = create_experiment (
                                    writer_nprocs           = n,
                                    reader_nprocs           = r,
                                    configFile              = config_fname,
                                    scalingType             = scaling,
                                    adios_xml_file          = adios_xml, 
                                    writer_decomposition    = n,
                                    reader_decomposition    = r,
                                    machine_name            = 'local',
                                    node_layout             = None,
                                    post_hoc                = post_hoc
                                    )
                    sweep_objs.append(sweep_obj)
        
            # we have created our sweep objects. Add them to the sweep group
            sg.parameter_groups = sweep_objs

            # Add this sweep group to the list that this function will return
            sweep_groups.append(sg)

    return sweep_groups

