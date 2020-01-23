from codar.cheetah import Campaign
from codar.cheetah import parameters as p
from codar.savanna.machines import SummitNode
import copy

def get_shared_node_layout (n_writers, n_readers):
    nc = SummitNode()
    for i in range(n_writers):
        nc.cpu[i] = "writer:{}".format(i)
    for i in range(n_readers):
        nc.cpu[i+n_writers] = "reader:{}".format(i)
    return [nc]

def get_separate_node_layout (n_writers, n_readers):
    nc_w = SummitNode()
    for i in range(n_writers):
        nc_w.cpu[i] = "writer:{}".format(i)

    nc_r = SummitNode()
    for i in range(n_readers):
        nc_r.cpu[i] = "reader:{}".format(i)

    return [nc_w,nc_r]

def get_sweeps(ref_params_d, n_writers):
    params_d = copy.deepcopy(ref_params_d)
    params_d['writer']['nprocs'].values=[n_writers]
    params_d['writer']['decomposition'].values=[n_writers]

    all_dicts = []
    all_sweeps = []

    # Loop over ratio of the no. of reader ranks
    for r in [8]:
        par_r = copy.deepcopy(params_d)
        par_r['reader']['nprocs'].values = [n_writers//r]
        par_r['reader']['decomposition'].values = [n_writers//r]

        # Loop over data size per process
        for d in ['512MB']:
            par_r_d = copy.deepcopy(par_r)
            par_r_d['writer']['configfile'].values = ['staging-perf-test-{}-{}to1.txt'.format(d,r)]
            par_r_d['reader']['configfile'].values = ['staging-perf-test-{}-{}to1.txt'.format(d,r)]

            # Loop over engines
            for e in ["bp4","sst-rdma","sst-tcp","ssc","insitumpi"]:
                par_r_d_e = copy.deepcopy(par_r_d)
                par_r_d_e['writer']['xmlfile'].values = ['staging-perf-test-{}.xml'.format(e)]
                par_r_d_e['reader']['xmlfile'].values = ['staging-perf-test-{}.xml'.format(e)]

                all_dicts.append(par_r_d_e)

    for d in all_dicts:
        sweep_params = []
        sweep_params.extend(list(d['writer'].values()))
        sweep_params.extend(list(d['reader'].values()))

        sep_node_layout = get_separate_node_layout(32, 32)
        shared_node_layout = None

        if d['writer']['nprocs'].values[0] // d['reader']['nprocs'].values[0] == 8:
            shared_node_layout = get_shared_node_layout(32,4)
        elif n_writers//32 < 4096:
             shared_node_layout = get_shared_node_layout(16,16)

        rc_dependency = None
        if 'bp4' in d['writer']['xmlfile'].values[0]:
            rc_dependency = {'reader': 'writer'}
        sweep_sep = p.Sweep(parameters = sweep_params, node_layout = {'summit':sep_node_layout}, rc_dependency=rc_dependency)

        sweep_shared = None
        if shared_node_layout:
            sweep_shared = p.Sweep(parameters = sweep_params, node_layout = {'summit':shared_node_layout}, rc_dependency=rc_dependency)

        if n_writers//32 < 4096:
            all_sweeps.append(sweep_sep)
        if sweep_shared:
            all_sweeps.append(sweep_shared)

    return all_sweeps


class Adios_iotest(Campaign):

    # A name for the campaign
    name = "ADIOS_IOTEST"

    # A list of the codes that will be part of the workflow
    # If there is an adios xml file associated with the codes, list it here
    codes = [ ("writer", dict(exe="adios_iotest")),
              ("reader", dict(exe="adios_iotest"))
            ]

    # A list of machines that this campaign must be supported on
    supported_machines = ['local', 'theta', 'summit']

    # Option to kill an experiment (just one experiment, not the full sweep or campaign) if one of the codes fails
    kill_on_partial_failure = True

    # Some pre-processing in the experiment directory
    # This is performed when the campaign directory is created (before the campaign is launched)
    run_dir_setup_script = None

    # A post-processing script to be run in the experiment directory after the experiment completes
    # For example, removing some large files after the experiment is done
    run_post_process_script = 'cleanup.sh'

    # umask applied to your directory in the campaign so that colleagues can view files
    umask = '027'

    # Scheduler information: job queue, account-id etc. Leave it to None if running on a local machine
    scheduler_options = {'theta':  {'project':'CSC249ADCD01', 'queue': 'batch'},
                         'summit': {'project':'csc303'}}

    # Setup your environment. Loading modules, setting the LD_LIBRARY_PATH etc.
    # Ensure this script is executable
    app_config_scripts = {'local': 'env_setup.sh', 'theta': 'env_setup.sh', 'summit':'env_setup.sh'}

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

    # Create the sweep parameters for a sweep
    params = {}
    params['writer'] = {}
    params['reader'] = {}

    params['writer']['nprocs']          = p.ParamRunner ('writer', 'nprocs', [])
    params['writer']['appid']           = p.ParamCmdLineOption ('writer', 'appid', '-a', [1])
    params['writer']['configfile']      = p.ParamCmdLineOption ('writer', 'configFile', '-c', [])
    params['writer']['scaling']         = p.ParamCmdLineOption ('writer', 'scaling', '-w', [None])
    params['writer']['xmlfile']         = p.ParamCmdLineOption ('writer', 'xmlfile', '-x', [])
    params['writer']['decomposition']   = p.ParamCmdLineOption ('writer', 'decomposition', '-d', [])

    params['reader']['nprocs']          = p.ParamRunner ('reader', 'nprocs', [])
    params['reader']['appid']           = p.ParamCmdLineOption ('reader', 'appid', '-a', [2])
    params['reader']['configfile']      = p.ParamCmdLineOption ('reader', 'configFile', '-c', [])
    params['reader']['scaling']         = p.ParamCmdLineOption ('reader', 'scaling', '-w', [None])
    params['reader']['xmlfile']         = p.ParamCmdLineOption ('reader', 'xmlfile', '-x', [])
    params['reader']['decomposition']   = p.ParamCmdLineOption ('reader', 'decomposition', '-d', [])

    sweeps = []
    for n in [8]:
        group_sweeps = get_sweeps (params, n*32)
        # pdb.set_trace()
        s_group = p.SweepGroup("{}-nodes".format(n),
                               walltime=7200,
                               per_run_timeout=600,
                               component_inputs={'writer':input_files},
                               #nodes=128,
                               parameter_groups=group_sweeps,)
        sweeps.append(s_group)

