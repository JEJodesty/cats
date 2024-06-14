import json, glob, os, multiprocessing, shutil, subprocess, tempfile, time
from copy import copy, deepcopy
from pprint import pprint

from cats.utils import subproc_run


class CoD:
    def __init__(self, INTEGRATION_INPUT_CACHE, cidDir):
        # self.JOB_HOME = JOB_HOME
        self.CAT_HOME = None
        self.INTEGRATION_INPUT_CACHE = INTEGRATION_INPUT_CACHE
        self.ingress_job_id = None
        self.ingressed_data_cid = None
        # self.integrated_data_cid = None
        self.cidDir = cidDir

    def contains_substring(self, substring):
        return lambda s: substring in s

    def cidDirUponCompletion(self, directory_path, job_id, check_interval=1, timeout=None):
        start_time = time.time()
        while self.checkStatusOfJob_printless(job_id=job_id) != "Completed":
            status = self.checkStatusOfJob(job_id=job_id)
            if status != "":
                print("job not completed: %s - %s" % (job_id, status))
                exit()
            # Check if timeout has been reached
            if timeout and (time.time() - start_time) > timeout:
                print(f"Timeout reached. Directory '{directory_path}' is still empty.")
                exit()
            time.sleep(check_interval)

        data_dir_cid = self.cidDir(directory_path)
        print("job output CIDed: %s" % data_dir_cid)
        return data_dir_cid

    def describeJob(self, job_id):
        cmd = f"bacalhau describe --json {job_id}"
        print(cmd)
        job_result = subproc_run(cmd)
        job_dict = json.loads(job_result.stdout)
        return job_dict

    def getJobState(self, job_id):
        return self.describeJob(job_id)['State']

    def getJobExecutions(self, job_id):
        return self.describeJob(job_id)['State']['Executions']

    def getPublishedURI(self, job_id):
        key_to_find = 'State'
        value_to_find = 'Completed'
        matching_execution = next(
            (d for d in self.getJobExecutions(job_id) if d.get(key_to_find) == value_to_find), None
        )
        return matching_execution['PublishedResults']

    def waitForJobCompletion(self, job_id, check_interval=1, timeout=None):
        start_time = time.time()
        while self.checkStatusOfJob_printless(job_id=job_id) != "Completed":
            status = self.checkStatusOfJob_printless(job_id)
            if status == "":
                print("job status is empty! %s" % job_id)
            elif status != "":
                print("job not completed: %s - %s" % (job_id, status))
            # Check if timeout has been reached
            if timeout and (time.time() - start_time) > timeout:
                print(f"Job Still Processing: %s - %s" % (job_id, status))
                return status
            time.sleep(check_interval)
        print("job completed: %s" % job_id)
        return self.checkStatusOfJob_printless(job_id)

    def checkStatusOfJob_printless(self, job_id: str) -> str:
        assert len(job_id) > 0
        cmd = f"bacalhau list --output json --id-filter {job_id}"
        p = subproc_run(cmd)
        r = self.parseJobStatus(p.stdout)
        return r

    # checkStatusOfJob checks the status of a Bacalhau job
    def checkStatusOfJob(self, job_id: str) -> str:
        r = self.checkStatusOfJob_printless(job_id)
        if r == "":
            print("job status is empty! %s" % job_id)
        elif r == "Completed":
            print("job completed: %s" % job_id)
        else:
            print("job not completed: %s - %s" % (job_id, r))
        return r

    def getCIDedResults(self, job_id: str, log_mode: str = "json", download_timeout_secs: str = "5m0s"):
        output_dir = self.CACHE_HOME
        # job_result.stdout
        cmd = f"bacalhau get {job_id} --output-dir {output_dir} --download-timeout-secs {download_timeout_secs}"
        print(cmd)
        job_result = subproc_run(cmd)
        print(job_result.stdout)
        job_dict = json.loads(job_result.stdout)
        return job_dict

    def codSubmit(self, cmd):
        submit = subproc_run(cmd)
        submit_job_id = submit.stdout.split('\n')[0]
        print("job submitted: %s" % submit_job_id)
        print()
        return submit_job_id

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


class MeshClient(CoD):
    def __init__(self, ipfsClient, filecoinClient=None, awsClient=None, CATS_HOME=None):
        self.CATS_HOME = None
        self.DATA_HOME = None
        self.JOB_HOME = None
        self.CACHE_HOME = None
        self.INPUT_HOME = None
        self.OUTPUT_HOME = None
        if CATS_HOME is not None:
            self.catStore(CATS_HOME)

        self.INGRESS_HOME = None
        self.INTEGRATION_HOME = None
        self.INTEGRATION_INPUT_CACHE = None
        self.INTEGRATION_INPUT_DATA_CACHE = None
        self.EGRESS_HOME = None

        self.CAT_HOME = None
        self.CAR_HOME = None
        self.ipfsClient = ipfsClient
        self.filecoinClient = filecoinClient
        self.awsClient = awsClient
        self.context = ...
        CoD.__init__(self, INTEGRATION_INPUT_CACHE=self.INTEGRATION_INPUT_CACHE, cidDir=self.cidDir)

    def catStore(self, CATS_HOME):
        self.CATS_HOME = CATS_HOME
        self.DATA_HOME = self.CATS_HOME + '/data'
        self.JOB_HOME = self.DATA_HOME + '/jobs'

    def catSubmit(self, order_request):
        print("Order:")
        order = json.loads(self.cat(order_request["order_cid"]))
        print()
        pprint(order)
        print()

        ppost = lambda args, endpoint: \
            f'curl -X POST -H "Content-Type: application/json" -d \\\n\'{json.dumps(**args)}\' {endpoint}'
        post = lambda args, endpoint: \
            'curl -X POST -H "Content-Type: application/json" -d \'' + json.dumps(**args) + f'\' {endpoint}'

        post_cmd = post({'obj': order_request}, order["endpoint"])
        print(ppost({'obj': order_request}, order["endpoint"]))
        print()
        response_str = subprocess.check_output(post_cmd, shell=True)
        output_bom = json.loads(response_str)

        output_bom['POST'] = post_cmd
        return output_bom

    def linkProcess(
            self,
            cat_response,
            ingress_subproc=None,
            integrated_subproc=None,
            egress_subproc=None,
            integration_cache_subproc=None,
            infrafunction_subproc=None
    ):
        flattened_bom = self.flatten_bom(cat_response)
        flat_bom = deepcopy(flattened_bom['flat_bom'])
        function_cids = flat_bom['invoice']['order']['flat']['function']
        function = {}
        if ingress_subproc is not None:
            function['ingress_subproc_cid'] = self.ipfsClient.add_pyobj(ingress_subproc)
        else:
            function['ingress_subproc_cid'] = function_cids['ingress_subproc_cid']
        if integrated_subproc is not None:
            function['integrated_subproc_cid'] = self.ipfsClient.add_pyobj(integrated_subproc)
        else:
            function['integrated_subproc_cid'] = function_cids['integrated_subproc_cid']
        if egress_subproc is not None:
            function['egress_subproc_cid'] = self.ipfsClient.add_pyobj(egress_subproc)
        else:
            function['egress_subproc_cid'] = function_cids['egress_subproc_cid']
        if integration_cache_subproc is not None:
            function['integration_cache_subproc_cid'] = self.ipfsClient.add_pyobj(integration_cache_subproc)
        else:
            function['integration_cache_subproc_cid'] = function_cids['integration_cache_subproc_cid']
        if infrafunction_subproc is not None:
            function['infrafunction_subproc_cid'] = self.ipfsClient.add_pyobj(infrafunction_subproc)
        else:
            function['infrafunction_subproc_cid'] = function_cids['infrafunction_subproc_cid']
        new_function_cid = self.ipfsClient.add_str(json.dumps(function))

        invoice = flat_bom['invoice']
        input_invoice = {'data_cid': invoice['data_cid']}
        new_invoice_cid = self.ipfsClient.add_str(json.dumps(input_invoice))

        order = invoice['order']
        order['function_cid'] = new_function_cid
        order['invoice_cid'] = new_invoice_cid
        del order['flat']
        order['endpoint'] = 'http://127.0.0.1:5000/cat/node/link'

        order_request = {'order_cid': self.ipfsClient.add_str(json.dumps(order))}
        return order_request

    def create_order_request(
            self,
            ingress_subproc,
            integrated_subproc,
            egress_subproc,
            integration_cache_subproc,
            data_dirpath,
            structure_filepath,
            endpoint='http://127.0.0.1:5000/cat/node/execute'
    ):
        structure_cid, structure_name = self.cidFile(structure_filepath)
        function = {
            'ingress_subproc_cid': self.ipfsClient.add_pyobj(ingress_subproc),
            'integrated_subproc_cid': self.ipfsClient.add_pyobj(integrated_subproc),
            'egress_subproc_cid': self.ipfsClient.add_pyobj(egress_subproc),
            'integration_cache_subproc_cid': self.ipfsClient.add_pyobj(integration_cache_subproc),
            'infrafunction_subproc_cid': None
        }
        invoice = {
            "data_cid": self.cidDir(data_dirpath)
        }
        order = {
            "function_cid": self.ipfsClient.add_str(json.dumps(function)),
            "structure_cid": structure_cid,
            "invoice_cid": self.ipfsClient.add_str(json.dumps(invoice)),
            "structure_filepath": structure_name,
            "JOB_HOME": self.JOB_HOME,
            "endpoint": endpoint
        }
        order_request = {
            'order_cid': self.ipfsClient.add_str(json.dumps(order))
        }
        return order_request

    def flatten_bom(self, bom_response):
        invoice = json.loads(
            self.cat(bom_response["bom"]["invoice_cid"])
        )
        invoice['order'] = json.loads(
            self.cat(invoice['order_cid']),
        )
        invoice['order']['flat'] = {
            'function': json.loads(self.cat(invoice['order']["function_cid"])),
            'invoice': json.loads(self.cat(invoice['order']["invoice_cid"]))
        }
        bom_response["flat_bom"] = {
            'invoice': invoice,
            'log': json.loads(
                self.cat(bom_response["bom"]["log_cid"])
            )
        }
        return bom_response

    def initBOMjson(self,
        structure_cid: str, structure_filepath: str, function_cid: str, init_data_cid: str,
        seed_cid=None
    ):
        init_invoice = {
            'order_cid': None,
            # 'data_cid': None,
            'seed_cid': seed_cid,
        }
        init_order = {
            'invoice_cid': None,
            'function_cid': function_cid,
            'structure_cid': structure_cid,
            'structure_filepath': structure_filepath
        }

        init_invoice_cid = self.ipfsClient.add_json(init_invoice)
        init_order['invoice_cid'] = init_invoice_cid
        init_order_cid = self.ipfsClient.add_json(init_order)

        invoice = copy(init_invoice)
        invoice['order_cid'] = init_order_cid
        invoice_cid = self.ipfsClient.add_json(invoice)

        init_bom = {
            'invoice_cid': invoice_cid,
            'log_cid': None,
            'init_data_cid': init_data_cid
        }
        init_bom_json_cid = self.ipfsClient.add_json(init_bom)
        return init_bom_json_cid

    def initBOMcar(self, structure_cid: str, structure_filepath: str, function_cid: str, init_data_cid: str, init_bom_filename: str, seed_cid=None):
        init_bom_json_cid = self.initBOMjson(structure_cid, structure_filepath, function_cid, init_data_cid)
        car_bom_cid, init_bom_json_cid = self.convertBOMtoCAR(init_bom_json_cid, init_bom_filename)
        return car_bom_cid, init_bom_json_cid

    def linkData(self, cid, subdir=' - outputs/'):
        cmd = f"ipfs ls {cid}"
        response = subprocess.check_output(cmd.split(' ')).decode()
        dirs = response.split('\n')
        res = [i for i in dirs if subdir in i]
        return res[0].split(' - ')[0]

    def get(self, cid: str, filepath: str, output: str = None):
        if output is None:
            output = self.CATS_HOME
        subprocess.check_output(
            f"ipfs get {cid} --output {output}/{filepath}",
            stderr=subprocess.STDOUT,
            shell=True,
            cwd=output
        )
        return filepath

    def cat(self, cid: str):
        return subprocess.check_output(['ipfs', 'cat', cid]).decode()

    def catObj(self, cid: str):
        return subprocess.check_output(['ipfs', 'cat', cid])

    def getCar(self, cid: str, filepath: str):
        subprocess.check_output(
            f"ipfs dag export {cid} > {filepath}",
            stderr=subprocess.STDOUT,
            shell=True
        )

    def getBom(self, cid: str, filepath: str):
        self.get(cid, filepath)
        bom = dict(json.loads(filepath))
        subprocess.check_output(
            f"rm {filepath}",
            stderr=subprocess.STDOUT,
            shell=True
        )
        return bom

    def BOMcarToIPFS(self, bom_cid: str, filepath: str):
        self.getCar(bom_cid, filepath)
        storage_bom_cid = self.ipfsClient.post_upload(filepath)
        return storage_bom_cid, bom_cid

    def convertBOMtoCAR(self, bom_cid: str, filepath: str):
        self.getCar(bom_cid, filepath)
        car_bom_cid = None
        try:
            car_bom_cid = self.ipfsClient.add(filepath)['Hash']
        except:
            for attrs in self.ipfsClient.add(filepath):
                if attrs['Name'] == filepath:
                    print(attrs)
                    car_bom_cid = attrs['Hash']
        return car_bom_cid, bom_cid

    def getEnhancedBom(self, bom_json_cid: str, INPUT_HOME: str = None, OUTPUT_HOME: str = None):
        if INPUT_HOME is None:
            INPUT_HOME = self.INPUT_HOME
        if OUTPUT_HOME is None:
            OUTPUT_HOME = self.OUTPUT_HOME
        self.CAR_HOME = OUTPUT_HOME + '/bom.car'
        self.get(cid=bom_json_cid, output=OUTPUT_HOME, filepath='bom.json')
        bom = json.loads(open(f'{OUTPUT_HOME}/bom.json', 'r').read())
        enhanced_bom = deepcopy(bom)
        enhanced_bom['bom_json_cid'] = bom_json_cid

        self.get(cid=bom['invoice_cid'], output=OUTPUT_HOME, filepath='invoice.json')
        enhanced_bom['invoice'] = json.loads(open(f'{OUTPUT_HOME}/invoice.json', 'r').read())

        self.get(cid=enhanced_bom['invoice']['order_cid'], output=INPUT_HOME, filepath='order.json')
        enhanced_bom['order'] = json.loads(open(f'{INPUT_HOME}/order.json', 'r').read())

        self.get(
            cid=enhanced_bom['order']['structure_cid'], output=INPUT_HOME,
            filepath=enhanced_bom['order']['structure_filepath']
        )
        return deepcopy(enhanced_bom), bom

    def createInvoice(self, orderCID: str, dataCID: str, seedCID: str):
        invoice = {'orderCID': orderCID, 'dataCID': dataCID, 'seedCID': seedCID}
        invoice_cid = self.ipfsClient.add_json(invoice)
        return invoice_cid

    def cidFile(self, filepath):
        file_json = self.ipfsClient.add(filepath)
        file_cid = file_json['Hash']
        file_name = file_json['Name']
        return file_cid, file_name

    def cidDir(self, filepath: str):
        data = self.ipfsClient.add(filepath, recursive=True)
        if type(data) is list:
            data_json = list(filter(lambda x: x['Name'] == 'outputs', data))[-1]
            data_cid = data_json['Hash']
            return data_cid
        else:
            data_json = data
            data_cid = data_json['Hash']
            return data_cid