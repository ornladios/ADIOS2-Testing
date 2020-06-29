from codar.cheetah import parameters as p

def create_experiment(writer_nprocs, reader_nprocs, config_file, adios_xml_file, writer_decomposition, reader_decomposition, machine_name, node_layout):
    """
    Creates a sweep object that tells Cheetah how to run the adios io test.
    Assumes 1D decomposition.
    """
    params = [
            # ParamRunner 'nprocs' specifies the no. of ranks to be spawned 
            p.ParamRunner       ('nwchem_main', 'nprocs', [writer_nprocs]),

            # Create a ParamCmdLineArg parameter to specify a command line argument to run the application
            p.ParamCmdLineOption   ('nwchem_main', 'app', '-a', [1]),
            p.ParamCmdLineOption   ('nwchem_main', 'app-config', '-c', [config_file]),
            p.ParamCmdLineOption   ('nwchem_main', 'adios-config', '-x', [adios_xml_file]),
            p.ParamCmdLineOption   ('nwchem_main', 'strongscaling', '-w', [None]),
            p.ParamCmdLineOption   ('nwchem_main', 'timing', '-t', [None]),
            p.ParamCmdLineOption   ('nwchem_main', 'decomposition', '-d', [writer_decomposition]),
            # Change the engine for the 'SimulationOutput' IO object in the adios xml file
            # p.ParamADIOS2XML    ('nwchem_main', 'dump_trajectory', 'trj_dump_out', 'engine', [ {'BP4':{'OpenTimeoutSecs':'30.0'}} ]),
            # Sweep over four values for the nprocs 
            p.ParamRunner       ('sorting', 'nprocs', [writer_nprocs]),
            p.ParamCmdLineOption   ('sorting', 'app', '-a', [2]),
            p.ParamCmdLineOption   ('sorting', 'app-config', '-c', [config_file]),
            p.ParamCmdLineOption   ('sorting', 'adios-config', '-x', [adios_xml_file]),
            p.ParamCmdLineOption   ('sorting', 'weakscaling', '-s', [None]),
            p.ParamCmdLineOption   ('sorting', 'timing', '-t', [None]),
            p.ParamCmdLineOption   ('sorting', 'decomposition', '-d', [reader_decomposition]),
            # Change the engine for the 'SimulationOutput' IO object in the adios xml file
            # p.ParamADIOS2XML    ('sorting', 'load_trajectory', 'trj_dump_in', 'engine', [ {'BP4':{'OpenTimeoutSecs':'30.0'}} ]),
    ]

    sweep = p.Sweep(parameters=params)
    # if node_layout:
    #     sweep.node_layout = {machine_name: node_layout}

    return sweep

