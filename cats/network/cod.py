import json, glob, os, multiprocessing, shutil, subprocess, tempfile, time
from datetime import datetime
from pathlib import Path
import re

from cats import JOB_HOME


class CoD:
    def __init__(self):
        self.JOB_HOME = JOB_HOME
        self.CAT_HOME = self.JOB_HOME + f"""cat={
            datetime.utcnow().isoformat()
        }"""
        Path(self.CAT_HOME).mkdir(parents=True, exist_ok=True)

    def contains_substring(self, substring):
        return lambda s: substring in s

    # checkStatusOfJob checks the status of a Bacalhau job
    def checkStatusOfJob(self, job_id: str) -> str:
        assert len(job_id) > 0
        p = subprocess.run(
            ["bacalhau", "list", "--output", "json", "--id-filter", job_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        r = self.parseJobStatus(p.stdout)
        if r == "":
            print("job status is empty! %s" % job_id)
        elif r == "Completed":
            print("job completed: %s" % job_id)
        else:
            print("job not completed: %s - %s" % (job_id, r))

        return r

    def ingress(self, input: str):
        print("Ingress:")
        cmd = f"bacalhau docker run --output ingress:/outputs -i {input} --id-only --wait alpine -- sh -c"
        cmd_list = cmd.split(' ') + ['cp -r /inputs/* /outputs/']
        submit = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=self.JOB_HOME
        )
        submit_job_id = submit.stdout.strip()
        print("job submitted: %s" % submit_job_id)

        if submit.returncode == 0:
            get_result = subprocess.run(
                f"bacalhau get {submit_job_id}".split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.CAT_HOME
            )
            get_result_list = get_result.stdout.splitlines()

            get_result_job_id_text = list(
                filter(self.contains_substring('have been written to...'), get_result_list)
            ).pop()
            get_result_job_id = re.findall(r"'(.*?)'", get_result_job_id_text).pop().replace("'", "")
            get_result_job_dir = list(filter(self.contains_substring('job-'), get_result_list)).pop()
            print("job submitted: %s" % get_result_job_id)
            if get_result.returncode != 0:
                print("failed (%d) job: %s" % (get_result.returncode, get_result_job_id))
        else:
            print("failed (%d) job: %s" % (submit.returncode, submit_job_id))

        job_ingress_dir = get_result_job_dir + '/ingress'
        return get_result_job_id

    def integrate(self, job_id: str):
        print("Integrate:")
        job_dir = '/job-' + job_id.split('-')[0]
        return self.CAT_HOME + job_dir + '/ingress/outputs/'

    def egress(self, integration_output_cid: str):
        print("Egress:")
        cmd = f"bacalhau docker run --output egress:/outputs -i {integration_output_cid} --id-only --wait alpine -- sh -c"
        cmd_list = cmd.split(' ') + ['cp -r /inputs/* /outputs/']
        submit = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=self.JOB_HOME
        )
        submit_job_id = submit.stdout.strip()
        print("job submitted: %s" % submit_job_id)

        if submit.returncode == 0:
            get_result = subprocess.run(
                f"bacalhau get {submit_job_id}".split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.CAT_HOME
            )
            get_result_list = get_result.stdout.splitlines()

            get_result_job_id_text = list(filter(self.contains_substring('have been written to...'), get_result_list)).pop()
            get_result_job_id = re.findall(r"'(.*?)'", get_result_job_id_text).pop().replace("'", "")
            get_result_job_dir = list(filter(self.contains_substring('job-'), get_result_list)).pop()
            if get_result.returncode != 0:
                print("failed (%d) job: %s" % (get_result.returncode, get_result_job_id))
        else:
            print("failed (%d) job: %s" % (submit.returncode, submit_job_id))

        job_egress_dir = get_result_job_dir + '/egress'
        return submit_job_id, job_egress_dir

    # submitJob submits a job to the Bacalhau network
    def submitJob(self, cid: str) -> str:
        assert len(cid) > 0
        p = subprocess.run(
            [
                "bacalhau",
                "docker",
                "run",
                "--id-only",
                "--wait=false",
                "--input",
                "ipfs://" + cid + ":/inputs/data.tar.gz",
                "ghcr.io/bacalhau-project/examples/blockchain-etl:0.0.6"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if p.returncode != 0:
            print("failed (%d) job: %s" % (p.returncode, p.stdout))
        job_id = p.stdout.strip()
        print("job submitted: %s" % job_id)

        return job_id

    # getResultsFromJob gets the results from a Bacalhau job
    def getResultsFromJob(self, job_id: str) -> str:
        assert len(job_id) > 0
        temp_dir = tempfile.mkdtemp()
        print("getting results for job: %s" % job_id)
        for i in range(0, 5): # try 5 times
            p = subprocess.run(
                [
                    "bacalhau",
                    "get",
                    "--output-dir",
                    temp_dir,
                    job_id,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if p.returncode == 0:
                break
            else:
                print("failed (exit %d) to get job: %s" % (p.returncode, p.stdout))

        return temp_dir

    # parseJobStatus parses the status of a Bacalhau job
    def parseJobStatus(self, result: str) -> str:
        if len(result) == 0:
            return ""
        r = json.loads(result)
        if len(r) > 0:
            return r[0]["State"]["State"]
        return ""

    # parseHashes splits lines from a text file into a list
    def parseHashes(self, filename: str) -> list:
        assert os.path.exists(filename)
        with open(filename, "r") as f:
            hashes = f.read().splitlines()
        return hashes

    def parseHashesFromFile(self, file: str, num_files: int = -1):
        # Use multiprocessing to work in parallel
        count = multiprocessing.cpu_count()
        with multiprocessing.Pool(processes=count) as pool:
            hashes = self.parseHashes(file)[:num_files]
            print("submitting %d jobs" % len(hashes))
            job_ids = pool.map(self.submitJob, hashes)
            assert len(job_ids) == len(hashes)

            print("waiting for jobs to complete...")
            while True:
                job_statuses = pool.map(self.checkStatusOfJob, job_ids)
                total_finished = sum(map(lambda x: x == "Completed", job_statuses))
                if total_finished >= len(job_ids):
                    break
                print("%d/%d jobs completed" % (total_finished, len(job_ids)))
                time.sleep(2)

            print("all jobs completed, saving results...")
            results = pool.map(self.getResultsFromJob, job_ids)
            print("finished saving results")

            # Do something with the results
            shutil.rmtree("../../results", ignore_errors=True)
            os.makedirs("../../results", exist_ok=True)
            for r in results:
                path = os.path.join(r, "outputs", "*.csv")
                csv_file = glob.glob(path)
                for f in csv_file:
                    print("moving %s to results" % f)
                    shutil.move(f, "../../results")
