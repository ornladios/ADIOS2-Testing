from codar.cheetah import Campaign
import small_summit_sweep_groups as small_summit_sg
import small_rhea_sweep_groups as small_rhea_sg


class Adios_iotest(Campaign):

    # Global campaign options
    name                    = "ADIOS_IOTEST"
    codes                   = [ ("writer", dict(exe="adios2_iotest")), ("reader", dict(exe="adios2_iotest")) ]
    supported_machines      = ['local', 'theta', 'summit', 'rhea']
    kill_on_partial_failure = True
    run_dir_setup_script    = None
    run_post_process_script = 'post-processing/cleanup.sh'
    umask                   = '027'
    scheduler_options       = {'theta':  {'project':'', 'queue': 'batch'}, 'rhea':  {'project':'csc143', 'queue': 'batch'}, 'summit': {'project':'csc303'}}
    app_config_scripts = {'local': 'env-setup/env_setup_local.sh', 'theta': 'env-setup/env_setup_theta.sh',
                          'rhea': 'env-setup/env_setup_rhea.sh', 'summit': 'env-setup/env_setup_summit.sh'}


    sweeps = {'summit': small_summit_sg.sweep_groups, 'rhea': small_rhea_sg.sweep_groups}

