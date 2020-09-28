from sweep_groups_helper import create_sweep_groups


# Parameters
x_np                    = [4]
g_np                    = [2]
c_np                    = [2]
engines                 = ['bp4', 'insitumpi', 'sst-tcp', 'ssc']
run_repetitions         = 0
batch_job_timeout_secs  = 3600
per_experiment_timeout  = 360


sweep_groups = create_sweep_groups ('local',
                                    x_np,
                                    g_np,
                                    c_np,
                                    engines,
                                    None,  # node layout
                                    run_repetitions,
                                    batch_job_timeout_secs,
                                    per_experiment_timeout)

