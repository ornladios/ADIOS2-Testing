from codar.cheetah import Campaign
import summit_sweep_groups as summit_sg
import local_sweep_groups as local_sg


class Adios2_iotest(Campaign):

    # Global campaign options
    name                    = "ADIOS2_IOTEST"
    codes                   = [ ("x", dict(exe="adios2_iotest")), ("g", dict(exe="adios2_iotest")) , ("c", dict(exe="adios2_iotest"))]
    supported_machines      = ['local', 'theta', 'summit']
    kill_on_partial_failure = True
    run_dir_setup_script    = None
    run_post_process_script = 'post-processing/cleanup.sh'
    umask                   = '027'
    scheduler_options       = {'theta':  {'project':'', 'queue': 'batch'}, 'summit': {'project':'csc143'}}
    app_config_scripts      = {'local': 'env-setup/env_setup_local.sh', 'theta': 'env-setup/env_setup_theta.sh', 'summit':'env-setup/env_setup_summit.sh'}

    sweeps = {'summit': summit_sg.sweep_groups, 'local': local_sg.sweep_groups}

