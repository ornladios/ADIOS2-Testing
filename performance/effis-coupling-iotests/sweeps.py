from codar.cheetah import parameters as p


def create_experiment(x_nprocs, g_nprocs, c_nprocs, configFile, scalingType, adios_xml_file, x_decomposition, g_decomposition, c_decomposition, machine_name, node_layout, post_hoc=False):
    """
    Creates a sweep object that tells Cheetah how to run the adios io test.
    Assumes 1D decomposition.
    """

    params = [
            p.ParamRunner('x', 'nprocs', [x_nprocs]),
            p.ParamRunner('g', 'nprocs', [g_nprocs]),
            p.ParamRunner('c', 'nprocs', [c_nprocs]),

            p.ParamCmdLineOption('x', 'appid', '-a', [1]),
            p.ParamCmdLineOption('x', 'configFile','-c', [configFile]),
            p.ParamCmdLineOption('x', 'scaling', scalingType, [None]),
            p.ParamCmdLineOption('x', 'adios_xml_file', '-x', [adios_xml_file]),
            p.ParamCmdLineOption('x', 'decomposition','-d',[x_decomposition]),
            p.ParamCmdLineOption('x', 'timing_info','-t',[None]),

            p.ParamCmdLineOption('g', 'appid', '-a', [2]),
            p.ParamCmdLineOption('g', 'configFile','-c', [configFile]),
            p.ParamCmdLineOption('g', 'scaling', scalingType, [None]),
            p.ParamCmdLineOption('g', 'adios_xml_file', '-x', [adios_xml_file]),
            p.ParamCmdLineOption('g', 'decomposition','-d',[g_decomposition]),
            p.ParamCmdLineOption('g', 'timing_info','-t',[None]),

            p.ParamCmdLineOption('c', 'appid', '-a', [3]),
            p.ParamCmdLineOption('c', 'configFile','-c', [configFile]),
            p.ParamCmdLineOption('c', 'scaling', scalingType, [None]),
            p.ParamCmdLineOption('c', 'adios_xml_file', '-x', [adios_xml_file]),
            p.ParamCmdLineOption('c', 'decomposition','-d',[c_decomposition]),
            p.ParamCmdLineOption('c', 'timing_info','-t',[None]),
            ]

    rc_dependency = None

    sweep = p.Sweep(parameters=params, rc_dependency=rc_dependency)
    if node_layout:
        sweep.node_layout = {machine_name: node_layout}

    return sweep

