from sweeps import create_experiment
from codar.cheetah.parameters import SweepGroup


input_files = [
    'config-files/staging-perf-test-many-vars.txt',
    'xml-files/staging-perf-test-sst-bp.xml',
    'xml-files/staging-perf-test-sst-ffs.xml'
]


def create_sweep_groups(machine_name, writer_np, reader_np_ratio, size_per_pe, engines, node_layouts,
        run_repetitions, batch_job_timeout_secs, per_experiment_timeout):
    """
    Create sweep groups for the input set of parameters.
    For each combination of writer ranks and ADIOS engines, a separate sweep group is created.
    E.g., 128-processes-bp4

    Input args:
    machine_name:           Name of the target machine. local/summit/theta etc.
    writer_np:              List of values for the number of writer ranks
    reader_np_ratio:        Ratio of the number of reader ranks to writer ranks
    size_per_pe:            Data size per process
    engines:                A List of ADIOS engines
    node_layouts:           A list of node layouts (on machines that support node layouts, otherwise None)
    run_repetitions:        No. of times each experiment must be repeated
    batch_job_timeout_secs: The total runtime for each sweep group
    per_experiment_timeout: Timeout for each experiment

    Returns - List of sweep groups
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
                    tau_profiling       = False,
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
                    
                    config_fname = "staging-perf-test-{}.txt".format(s,r_ratio)
                    scaling = '-w'
                    adios_xml = 'staging-perf-test-{}.xml'.format(e)
                    post_hoc = True if 'bp4' in e else False

                    # Ugh. Need a better way to iterate over node layouts if it is not None
                    if node_layouts:
                        for nl in node_layouts:

                            # create a parameter sweep object for this parameter combination
                            sweep_obj = create_experiment (
                                            writer_nprocs           = n,
                                            reader_nprocs           = r,
                                            configFile              = config_fname,
                                            scalingType             = scaling,
                                            adios_xml_file          = adios_xml, 
                                            writer_decomposition    = n,
                                            reader_decomposition    = r,
                                            machine_name            = machine_name,
                                            node_layout             = nl,
                                            post_hoc                = post_hoc
                                            )
                            sweep_objs.append(sweep_obj)
                    else:
                        # create a parameter sweep object for this parameter combination
                        sweep_obj = create_experiment (
                                        writer_nprocs           = n,
                                        reader_nprocs           = r,
                                        configFile              = config_fname,
                                        scalingType             = scaling,
                                        adios_xml_file          = adios_xml, 
                                        writer_decomposition    = n,
                                        reader_decomposition    = r,
                                        machine_name            = machine_name,
                                        node_layout             = None,
                                        post_hoc                = post_hoc
                                        )
                        sweep_objs.append(sweep_obj)

        
            # we have created our sweep objects. Add them to the sweep group
            sg.parameter_groups = sweep_objs

            # Add this sweep group to the list that this function will return
            sweep_groups.append(sg)

    return sweep_groups

