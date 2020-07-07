from codar.cheetah import Campaign
from codar.cheetah import parameters as p

from datetime import timedelta


class PlanarReadqCampaign(Campaign):

    name = "planar"

    codes = [ ("app1",  dict(exe="adios2_iotest",         adios_xml_file='adios2.xml', sleep_after=5)),
              ("app2", dict(exe="adios2_iotest",  adios_xml_file='adios2.xml', runner_override=False))
            ]

    run_dir_setup_script = "planar_reads.sh"

    supported_machines = ['local', 'cori', 'titan', 'theta']

    scheduler_options = {
        "cori": {
            "queue": "debug",
            "constraint": "haswell",
            "license": "SCRATCH,project",
        },
        "titan": {
            "queue": "debug",
            "project": "csc242",
        },
        "theta": {
            "queue": "debug-flat-quad",
            "project": "CSC249ADCD01",
        }
    }

    umask = '027'

    sweeps = [
     p.SweepGroup(name="all-methods", nodes=2,
                  walltime=timedelta(minutes=30),
      parameter_groups=
      [p.Sweep([
        p.ParamRunner("app1", "nprocs", [8]),
        p.ParamRunner("app2", "nprocs", [8]),
        p.ParamCmdLineOption("app1", "app ID", "-a", [1]),
        p.ParamCmdLineOption("app1", "config file", "-c", ["planar_reads.txt"]),
        p.ParamCmdLineOption("app1", "adios xml", "-x", ["adios2.xml"]),
        p.ParamCmdLineArg("app1", "weak scaling", 1, ["-w"]),
        p.ParamCmdLineOption("app1", "rank decomp", "-D", ["1,1,1"]), 
        p.ParamCmdLineOption("app2", "app ID", "-a", [2]),
        p.ParamCmdLineOption("app2", "config file", "-c", ["planar_reads.txt"]),
        p.ParamCmdLineOption("app2", "adios xml", "-x", ["adios2.xml"]),
        p.ParamCmdLineArg("app2", "weak scaling", 1, ["-w"]),
        p.ParamCmdLineOption("app2", "rank decomp", "-D", ["1,1,1"]),
        p.ParamEnvVar("app1", "cube length", "CUBE_LEN", [40]),
        p.ParamEnvVar("app1", "read pattern", "READ_PATTERN", ["ij", "ik", "jk", "chunk"])
        ]),
      ]),
    ]
