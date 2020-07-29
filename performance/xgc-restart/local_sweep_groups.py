from sweep_groups_helper import create_sweep_groups


# Parameters
writer_np               = [4,8]
reader_np_ratio         = [1]
size_per_pe             = []
engines                 = ['bp4']
run_repetitions         = 0
batch_job_timeout_secs  = 3600
per_experiment_timeout  = 600


sweep_groups = create_sweep_groups ('local',
                                    writer_np,
                                    reader_np_ratio,
                                    size_per_pe,
                                    engines,
                                    None,  # node layout
                                    run_repetitions,
                                    batch_job_timeout_secs,
                                    per_experiment_timeout)

