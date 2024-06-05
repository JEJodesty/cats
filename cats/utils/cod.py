from cats.utils import subproc_run


def codSubmit(cmd: str):
    submit = subproc_run(cmd)
    submit_job_id = submit.stdout.split('\n')[0]
    print("job submitted: %s" % submit_job_id)
    print()
    return submit_job_id
