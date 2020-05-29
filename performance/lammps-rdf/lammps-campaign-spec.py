import math
from codar.cheetah import Campaign
from codar.cheetah import parameters as p
from codar.savanna.machines import SummitNode
from codar.cheetah.parameters import SymLink
import node_layouts as node_layouts
import sweeps as sweeps
import copy


class LAMMPS(Campaign):
    name = "lammps"

    codes = [ ("simulation", dict(exe="lmp", adios_xml_file='adios2_config.xml')),
              ("rdf_calc", dict(exe="lmp", adios_xml_file='adios2_config.xml')), 
              ("sim_inline_rdf_calc", dict(exe="lmp", adios_xml_file='adios2_config.xml')),]

    supported_machines = ['local', 'titan', 'theta', 'summit']
    kill_on_partial_failure = True
    run_dir_setup_script = None
    run_post_process_script = None
    umask = '027'
    scheduler_options = {'theta': {'project':'CSC249ADCD01', 'queue': 'default'},
                         'summit': {'project':'csc303'}}
    app_config_scripts = {'local': 'setup.sh', 'theta': 'env_setup.sh', 'summit':'env-setup.sh'}

    sim_nodes = [1, 2]
    analysis_nodes = [1]
    sweeps = []
    sg_count = 1
    for s in sim_nodes:
        for a in analysis_nodes:
            if a > s:
                continue
            sw_inline = sweeps.inline_analysis(42*(s+a))
            sw_posthoc = sweeps.posthoc_analysis(42*s, 42*a)
            sw_insitu_sst_sep_nodes = sweeps.insitu_analysis(42*s, 42*a, node_layouts.separate_nodes(), 'SST')
            sw_insitu_sst_shared_nodes_21to21 = sweeps.insitu_analysis(21*(s+a), 21*(s+a), node_layouts.share_nodes_21to21(), 'SST')
            sw_insitu_sst_shared_nodes_28to14 = sweeps.insitu_analysis(28*(s+a), 14*(s+a), node_layouts.share_nodes_28to14(), 'SST')
            sw_insitu_sst_shared_nodes_35to7 = sweeps.insitu_analysis(35*(s+a), 7*(s+a), node_layouts.share_nodes_35to7(), 'SST')
            sw_insitu_sst_shared_nodes_40to2 = sweeps.insitu_analysis(40*(s+a), 2*(s+a), node_layouts.share_nodes_40to2(), 'SST')
            sw_insitu_bp4_sep_nodes = sweeps.insitu_analysis(42*s, 42*a, node_layouts.separate_nodes(), 'BP4')
            sw_insitu_bp4_shared_nodes_21to21 = sweeps.insitu_analysis(21*(s+a), 21*(s+a), node_layouts.share_nodes_21to21(), 'BP4')
            sw_insitu_bp4_shared_nodes_28to14 = sweeps.insitu_analysis(28*(s+a), 14*(s+a), node_layouts.share_nodes_28to14(), 'BP4')
            sw_insitu_bp4_shared_nodes_35to7 = sweeps.insitu_analysis(35*(s+a), 7*(s+a), node_layouts.share_nodes_35to7(), 'BP4')
            sw_insitu_bp4_shared_nodes_40to2 = sweeps.insitu_analysis(40*(s+a), 2*(s+a), node_layouts.share_nodes_40to2(), 'BP4')
        

            # Create a SweepGroup and add the above Sweeps. Set batch job properties such as the no. of nodes, 
            sweepGroup = p.SweepGroup ("sg-"+str(sg_count),
                                walltime=1200,
                                per_run_timeout=200,
                                parameter_groups=[sw_inline, sw_posthoc, sw_insitu_sst_sep_nodes, sw_insitu_sst_shared_nodes_21to21, sw_insitu_sst_shared_nodes_28to14, sw_insitu_sst_shared_nodes_35to7, sw_insitu_sst_shared_nodes_40to2, sw_insitu_bp4_sep_nodes, sw_insitu_bp4_shared_nodes_21to21, sw_insitu_bp4_shared_nodes_28to14, sw_insitu_bp4_shared_nodes_35to7, sw_insitu_bp4_shared_nodes_40to2],
                                launch_mode='default',
                                #nodes=16,
                                component_inputs = {'simulation': ['in.lj.nordf'], 'rdf_calc': ['in.lj.rdf.rerun'], 'sim_inline_rdf_calc': ['in.lj.rdf.nodump']},
                                run_repetitions=2, )
    
            sg_count += 1
            # Activate the SweepGroup
            sweeps.append(sweepGroup)

