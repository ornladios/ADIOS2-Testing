from codar.cheetah import Campaign
import theta_sweep_groups as theta_sg

class Adios_iotest(Campaign):

    # Global campaign options
    name                    = "ADIOS_IOTEST_NWCHEM"
    codes                   = [ ("writer", dict(exe="/home/xliang/ornl/utils/adios2/bin/adios2_iotest", adios_xml_file='copro.xml')), ("reader", dict(exe="/home/xliang/ornl/utils/adios2/bin/adios2_iotest", adios_xml_file='copro.xml')) ]
    supported_machines      = ['rhea', 'theta', 'summit']
    kill_on_partial_failure = True
    run_dir_setup_script    = None
    run_post_process_script = 'post-processing/cleanup.sh'
    umask                   = '027'
    scheduler_options       = {'rhea': {'project':'csc143'}, 'theta':  {'project':'CSC250STDM11', 'queue': 'batch'}, 'summit': {'project':'csc303'}}
    app_config_scripts      = {'rhea': 'env-setup/env_setup_rhea.sh', 'theta': 'env-setup/env_setup_theta.sh', 'summit':'env-setup/env_setup_summit.sh'}

    sweeps = {'theta': theta_sg.sweep_groups}

