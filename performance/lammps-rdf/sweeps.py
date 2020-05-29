from codar.cheetah import parameters as p
import node_layouts as node_layouts

#----------------------------------------------------------------------------#
def inline_analysis(sim_nprocs):
    sweep_parameters = [
            p.ParamRunner       ('sim_inline_rdf_calc', 'nprocs', [sim_nprocs]),
            p.ParamCmdLineOption   ('sim_inline_rdf_calc', 'input', '-in', ["in.lj.rdf.nodump"]),
    ]
    sweep = p.Sweep (parameters    = sweep_parameters,
                     rc_dependency = None,
                     node_layout   = {'summit': node_layouts.all_sim_nodes()})
    return sweep


#----------------------------------------------------------------------------#
def posthoc_analysis(sim_nprocs, analysis_nprocs):
    sweep_parameters = [
            p.ParamRunner       ('simulation', 'nprocs', [sim_nprocs]),
            p.ParamCmdLineOption   ('simulation', 'sim input', '-in', ["in.lj.nordf"]),
            p.ParamADIOS2XML    ('simulation', 'sim output engine', 'custom', 'engine', [ {'BP4':{}} ]),

            p.ParamRunner       ('rdf_calc', 'nprocs', [analysis_nprocs]),
            p.ParamCmdLineOption   ('rdf_calc', 'input', '-in', ["in.lj.rdf.rerun"]),
    ]

    sweep = p.Sweep (parameters    = sweep_parameters,
                     rc_dependency = {'rdf_calc':'simulation'},
                     node_layout   = {'summit': node_layouts.separate_nodes()})

    return sweep


#----------------------------------------------------------------------------#
def insitu_analysis(sim_nprocs, analysis_nprocs, node_layout, adios_engine):
    sweep_parameters = [
            p.ParamRunner       ('simulation', 'nprocs', [sim_nprocs]),
            p.ParamCmdLineOption   ('simulation', 'sim input', '-in', ["in.lj.nordf"]),
            p.ParamADIOS2XML    ('simulation', 'sim output engine', 'custom', 'engine', [ {adios_engine:{}} ]),

            p.ParamRunner       ('rdf_calc', 'nprocs', [analysis_nprocs]),
            p.ParamCmdLineOption   ('rdf_calc', 'input', '-in', ["in.lj.rdf.rerun"]),
            p.ParamADIOS2XML    ('rdf_calc', 'analysis input engine', 'read_dump', 'engine', [ {adios_engine:{}} ]),
    ]

    sweep = p.Sweep (parameters    = sweep_parameters,
                     rc_dependency = None,
                     node_layout   = {'summit': node_layout})

    return sweep


