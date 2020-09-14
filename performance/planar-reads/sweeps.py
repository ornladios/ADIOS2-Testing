from codar.cheetah import parameters as p


def create_experiment(writer_nprocs, reader_nprocs, configFile, scalingType, adios_xml_file, writer_decomposition, reader_decomposition, machine_name, node_layout, cube_lengths, post_hoc=False):
    """
    Creates a sweep object that tells Cheetah how to run the adios io test using various different decompositions
    """
    
    params = [
            p.ParamRunner('writer', 'nprocs', [writer_nprocs]),
            p.ParamRunner('reader', 'nprocs', [reader_nprocs]),
    
            p.ParamCmdLineOption('writer', 'appid', '-a', [1]),
            p.ParamCmdLineOption('writer', 'configFile','-c', [configFile]),
            p.ParamCmdLineOption('writer', 'scaling', scalingType, [None]),
            p.ParamCmdLineOption('writer', 'adios_xml_file', '-x', [adios_xml_file]),
            p.ParamCmdLineOption('writer', 'decomposition','-D',[writer_decomposition]),
            p.ParamCmdLineOption('writer', 'timing_info','-t',[None]),
            p.ParamEnvVar('writer', 'cube_length', "CUBE_LEN", cube_lengths),
            p.ParamEnvVar('writer', 'read_pattern', "READ_PATTERN", ['ij', 'ik', 'jk', 'chunk']),
    
            p.ParamCmdLineOption('reader', 'appid', '-a', [2]),
            p.ParamCmdLineOption('reader', 'configFile','-c', [configFile]),
            p.ParamCmdLineOption('reader', 'scaling', scalingType, [None]),
            p.ParamCmdLineOption('reader', 'adios_xml_file', '-x', [adios_xml_file]),
            p.ParamCmdLineOption('reader', 'decomposition','-D',[reader_decomposition]),
            p.ParamCmdLineOption('reader', 'timing_info','-t',[None]),
            ]

    rc_dependency = None
    if post_hoc:
        rc_dependency = {'reader': 'writer'}

    sweep = p.Sweep(parameters=params, rc_dependency=rc_dependency)
    if node_layout:
        sweep.node_layout = {machine_name: node_layout}

    return sweep

