from codar.cheetah import Campaign
import rhea_sweep_groups as rhea_sg

class Adios_iotest(Campaign):

    # Global campaign options
    name                    = "ADIOS_IOTEST_NWCHEM"
    codes                   = [ ("writer", dict(exe="/ccs/home/xinliang/utils/adios/bin/adios2_iotest", adios_xml_file='copro.xml')), ("reader", dict(exe="/ccs/home/xinliang/utils/adios/bin/adios2_iotest", adios_xml_file='copro.xml')) ]
    supported_machines      = ['rhea', 'theta', 'summit']
    kill_on_partial_failure = True
    run_dir_setup_script    = None
    run_post_process_script = 'post-processing/cleanup.sh'
    umask                   = '027'
    scheduler_options       = {'rhea': {'project':'csc143'}, 'theta':  {'project':'', 'queue': 'batch'}, 'summit': {'project':'csc303'}}
    app_config_scripts      = {'rhea': 'env-setup/env_setup_rhea.sh', 'theta': 'env-setup/env_setup_theta.sh', 'summit':'env-setup/env_setup_summit.sh'}

    # sweeps = {'summit': summit_sg.sweep_groups, 'local': local_sg.sweep_groups}
    sweeps = {'rhea': rhea_sg.sweep_groups}

