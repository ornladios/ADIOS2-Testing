from sweeps import create_experiment
from codar.cheetah.parameters import SweepGroup


input_files = [
    'config-files/effis-coupling-xcg.txt',
    'config-files/effis-coupling-xg.txt',
    'config-files/effis-coupling-xgn.txt',
    'xml-files/effis-coupling-xcg-bp4.xml',
    'xml-files/effis-coupling-xg-bp4.xml',
    'xml-files/effis-coupling-xgn-bp4.xml',
    'xml-files/effis-coupling-xcg-insitumpi.xml',
    'xml-files/effis-coupling-xg-insitumpi.xml',
    'xml-files/effis-coupling-xgn-insitumpi.xml',
    'xml-files/effis-coupling-xcg-ssc.xml',
    'xml-files/effis-coupling-xg-ssc.xml',
    'xml-files/effis-coupling-xgn-ssc.xml',
    'xml-files/effis-coupling-xcg-sst-tcp.xml',
    'xml-files/effis-coupling-xg-sst-tcp.xml',
    'xml-files/effis-coupling-xgn-sst-tcp.xml'
]


def create_sweep_groups(machine_name, x_np, g_np, c_np, engines, node_layouts,
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

    if len(x_np) != len(g_np) or len(x_np) != len(c_np):
        print(x_np, g_np, c_np)
        exit()

    for mode in ["xcg", "xg", "xgn"]:
        for i in range(len(x_np)):
            for e in engines:
                # Create a separate sweep group (batch job) for different values of writer nprocs
                sg = SweepGroup(
                        name                = "{}-{}-{}-{}-{}".format(mode, x_np[i], g_np[i], c_np[i], e),
                        walltime            = batch_job_timeout_secs,
                        per_run_timeout     = per_experiment_timeout,
                        component_inputs    = {'x': input_files},
                        run_repetitions     = run_repetitions,
                        tau_profiling       = False,
                        parameter_groups    = None
                        )

                # Set launch mode to mpmd for insitumpi and ssc runs
                if 'insitumpi' in e: sg.launch_mode = 'mpmd'
                if 'ssc' in e: sg.launch_mode = 'mpmd'

                # Now lets create and add a list of sweep objects to this sweep group
                sweep_objs = []

                # Sweep over data size per process, engines, and the readers_ratio


                config_fname = "effis-coupling-{}.txt".format(mode)
                scaling = '-s'
                adios_xml = 'effis-coupling-{}-{}.xml'.format(mode,e)

                # Ugh. Need a better way to iterate over node layouts if it is not None
                layouts = node_layouts or [None]
                for nl in layouts:

                    # create a parameter sweep object for this parameter combination
                    sweep_obj = create_experiment (
                                    x_nprocs                = x_np[i],
                                    g_nprocs                = g_np[i],
                                    c_nprocs                = c_np[i],
                                    configFile              = config_fname,
                                    scalingType             = scaling,
                                    adios_xml_file          = adios_xml,
                                    x_decomposition         = x_np[i],
                                    g_decomposition         = g_np[i],
                                    c_decomposition         = c_np[i],
                                    machine_name            = machine_name,
                                    node_layout             = nl,
                                    post_hoc                = False
                                    )
                    sweep_objs.append(sweep_obj)

                # we have created our sweep objects. Add them to the sweep group
                sg.parameter_groups = sweep_objs

                # Add this sweep group to the list that this function will return
                sweep_groups.append(sg)

    return sweep_groups

