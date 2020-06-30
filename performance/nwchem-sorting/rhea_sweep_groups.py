from summit_node_layouts import summit_node_layouts


def create_sweep_groups(machine_name, writer_np, reader_np, engines, node_layouts, adios_xml_file, config_file,
        run_repetitions, batch_job_timeout_secs, per_experiment_timeout):
    """
    Create sweep groups for the input set of parameters.
    For each combination of writer ranks and ADIOS engines, a separate sweep group is created.
    E.g., 128-processes-bp4

    Input args:
    machine_name:           Name of the target machine. local/summit/theta etc.
    writer_np:              List of values for the number of writer ranks
    reader_np:              List of values for the number of reader ranks
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
        for r in reader_np:
            for e in engines:
                # Create a separate sweep group (batch job) for different values of writer nprocs
                sg = SweepGroup(
                        name                = "{}-writers-{}-readers-{}".format(n, r, e),
                        walltime            = batch_job_timeout_secs,
                        per_run_timeout     = per_experiment_timeout,
                        component_inputs    = {'writer': config_file},
                        run_repetitions     = run_repetitions,
                        tau_profiling       = True,
                        parameter_groups    = None
                        )
                # Set launch mode to mpmd for insitumpi runs
                # if 'insitumpi' in e: sg.launch_mode = 'mpmd'
                # Now lets create and add a list of sweep objects to this sweep group
                sweep_objs = []
                # TODO: add node_layout
                # create a parameter sweep object for this parameter combination
                sweep_obj = create_experiment (
                                writer_nprocs           = n,
                                reader_nprocs           = r,
                                configFile              = config_file,
                                adios_xml_file          = adios_xml_file, 
                                writer_decomposition    = n,
                                reader_decomposition    = r,
                                machine_name            = machine_name,
                                node_layout             = None,
                                )
                sweep_objs.append(sweep_obj)

            
                # we have created our sweep objects. Add them to the sweep group
                sg.parameter_groups = sweep_objs

                # Add this sweep group to the list that this function will return
                sweep_groups.append(sg)

    return sweep_groups

# Parameters
writer_np               = [80]
reader_np               = [8]
engines                 = [ {'BP4':{'OpenTimeoutSecs':'30.0'}}, {'SST':{}}, {"Null":{}}, {'BP4':{'OpenTimeoutSecs':'30.0', 'BurstBufferPath':'/tmp'}} ]
adios_xml_file          = 'copro.xml'
config_file             = 'copro-80.txt'
run_repetitions         = 1
batch_job_timeout_secs  = 3600
per_experiment_timeout  = 600


# node_layouts = summit_node_layouts('writer', 'reader')
node_layouts = []

sweep_groups = create_sweep_groups ('rhea',
                                    writer_np,
                                    reader_np,
                                    engines,
                                    node_layouts,
                                    adios_xml_file,
                                    config_file,
                                    run_repetitions,
                                    batch_job_timeout_secs,
                                    per_experiment_timeout)


