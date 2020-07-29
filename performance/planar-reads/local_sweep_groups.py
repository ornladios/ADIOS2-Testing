from sweep_groups_helper import create_sweep_groups


# Parameters
writer_np               = [8]
reader_np_ratio         = [1]
engines                 = ['bp4', 'insitumpi', 'sst-tcp']
run_repetitions         = 0
batch_job_timeout_secs  = 3600
cube_lengths            = ['16']
per_experiment_timeout  = 600


sweep_groups = create_sweep_groups ('local',
                                    writer_np,
                                    reader_np_ratio,
                                    engines,
                                    None,  # node layout
                                    cube_lengths,
                                    run_repetitions,
                                    batch_job_timeout_secs,
                                    per_experiment_timeout)

