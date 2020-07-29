from codar.cheetah import Campaign
#import summit_sweep_groups as summit_sg
import local_sweep_groups as local_sg


class PlanarReadCampaign(Campaign):

    # Global campaign options
    name                    = "Read_Patterns"
    codes                   = [ ("writer", dict(exe="adios2_iotest")), ("reader", dict(exe="adios2_iotest")) ]
    supported_machines      = ['local']
    kill_on_partial_failure = True
    run_dir_setup_script    = "planar_reads.sh"
    #run_post_process_script = 'post-processing/cleanup.sh'
    umask                   = '027'
    scheduler_options       = {'theta':  {'project':'', 'queue': 'batch'}, 'summit': {'project':'csc303'}}
    #app_config_scripts      = {'local': 'env-setup/env_setup_local.sh', 'theta': 'env-setup/env_setup_theta.sh', 'summit':'env-setup/env_setup_summit.sh'}

    sweeps = {'local': local_sg.sweep_groups}

