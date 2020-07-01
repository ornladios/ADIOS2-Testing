from codar.cheetah import parameters as p

def create_experiment(writer_nprocs, reader_nprocs, config_file, adios_xml_file, engine, writer_decomposition, reader_decomposition, machine_name, node_layout):
    """
    Creates a sweep object that tells Cheetah how to run the adios io test.
    Assumes 1D decomposition.
    """
    # print(adios_xml_file)
    # print(engine)
    params = [
            # ParamRunner 'nprocs' specifies the no. of ranks to be spawned 
            p.ParamRunner       ('writer', 'nprocs', [writer_nprocs]),
            # Create a ParamCmdLineArg parameter to specify a command line argument to run the application
            p.ParamCmdLineOption   ('writer', 'app', '-a', [1]),
            p.ParamCmdLineOption   ('writer', 'app-config', '-c', [config_file]),
            p.ParamCmdLineOption   ('writer', 'adios-config', '-x', [adios_xml_file]),
            p.ParamCmdLineOption   ('writer', 'strongscaling', '-w', [None]),
            p.ParamCmdLineOption   ('writer', 'timing', '-t', [None]),
            p.ParamCmdLineOption   ('writer', 'decomposition', '-d', [writer_decomposition]),
            # Change the engine for the 'SimulationOutput' IO object in the adios xml file
            p.ParamADIOS2XML    ('writer', 'dump_trajectory', 'trj_dump_out', 'engine', [engine]),
            # Sweep over four values for the nprocs 
            p.ParamRunner       ('reader', 'nprocs', [reader_nprocs]),
            p.ParamCmdLineOption   ('reader', 'app', '-a', [2]),
            p.ParamCmdLineOption   ('reader', 'app-config', '-c', [config_file]),
            p.ParamCmdLineOption   ('reader', 'adios-config', '-x', [adios_xml_file]),
            p.ParamCmdLineOption   ('reader', 'weakscaling', '-s', [None]),
            p.ParamCmdLineOption   ('reader', 'timing', '-t', [None]),
            p.ParamCmdLineOption   ('reader', 'decomposition', '-d', [reader_decomposition]),
            # Change the engine for the 'SimulationOutput' IO object in the adios xml file
            p.ParamADIOS2XML    ('reader', 'load_trajectory', 'trj_dump_in', 'engine', [engine]),
    ]

    sweep = p.Sweep(parameters=params)
    if node_layout:
        sweep.node_layout = {machine_name: node_layout}

    return sweep

