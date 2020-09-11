from codar.cheetah import Campaign
import local_sweep_groups as local_sg
import rhea_medium_sweep_groups as rhea_medium_sg
import rhea_small_sweep_groups as rhea_small_sg
import summit_medium_sweep_groups as summit_medium_sg
import summit_small_sweep_groups as summit_small_sg


class Adios_iotest(Campaign):

    # Global campaign options
    name = "ADIOS_IOTEST"
    codes = [("writer", dict(exe="adios2_iotest")),
             ("reader", dict(exe="adios2_iotest"))]
    supported_machines = ['local', 'theta', 'rhea', 'rheasmall', 'summit', 'summitsmall']
    kill_on_partial_failure = True
    run_dir_setup_script = None
    run_post_process_script = 'post-processing/cleanup.sh'
    umask = '027'
    scheduler_options = {
        'theta':  {'project': '', 'queue': 'batch'},
        'rhea':  {'project': 'csc143', 'queue': 'batch'},
        'rheasmall':  {'project': 'csc143', 'queue': 'batch'},
        'summit': {'project': 'csc303'},
        'summitsmall': {'project': 'csc303'}}

    app_config_scripts = {
        'local': 'env-setup/env_setup_local.sh',
        'theta': 'env-setup/env_setup_theta.sh',
        'rhea': 'env-setup/env_setup_rhea.sh',
        'rheasmall': 'env-setup/env_setup_rhea.sh',
        'summit': 'env-setup/env_setup_summit.sh',
        'summitsmall': 'env-setup/env_setup_summit.sh'}

    sweeps = {
        'local': local_sg.sweep_groups,
        'rhea': rhea_medium_sg.sweep_groups,
        'rheasmall': rhea_small_sg.sweep_groups,
        'summit': summit_medium_sg.sweep_groups,
        'summitsmall': summit_small_sg.sweep_groups }
