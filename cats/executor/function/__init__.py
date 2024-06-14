import json, pickle
from cats.utils import wait_for_directory


class InfraFunction:
    def __init__(self, service):
        self.service = service
        self.enhanced_bom = self.service.enhanced_bom
        self.function = json.loads(self.service.meshClient.cat(self.enhanced_bom['order']['function_cid']))
        self.ingress_subproc = pickle.loads(self.service.meshClient.catObj(self.function['ingress_subproc_cid']))
        self.integrated_subproc = pickle.loads(self.service.meshClient.catObj(self.function['integrated_subproc_cid']))
        self.egress_subproc = pickle.loads(self.service.meshClient.catObj(self.function['egress_subproc_cid']))
        self.integration_cache_subproc = pickle.loads(
            self.service.meshClient.catObj(self.function['integration_cache_subproc_cid'])
        )


class Processor(InfraFunction):
    def __init__(self, service):
        self.service = service
        InfraFunction.__init__(self, service=self.service)
        self.invoice_data_cid = None

        self.ingress_job_id = None
        self.ingress_input_data_cid = self.enhanced_bom['init_data_cid']
        self.integration_output = None
        self.integration_output_ipfs = None
        self.egress_job_id = None

    def Ingress_SubProc(self):
        self.ingress_job_id = self.ingress_subproc(input_dir=self.ingress_input_data_cid)
        self.service.INGRESS_JOB_STATUS = self.service.meshClient.waitForJobCompletion(
            self.ingress_job_id, check_interval=1, timeout=None
        )
        published_results = self.service.meshClient.getPublishedURI(self.ingress_job_id)
        self.service.meshClient.INGRESS_HOME = published_results['CID']
        self.service.INGRESS_EXIT_CODE = self.service.meshClient.cat(self.service.meshClient.INGRESS_HOME + "/exitCode")
        self.service.INGRESS_DATA_HOME = f'ipfs://{self.service.meshClient.INGRESS_HOME}/outputs'
        return self.ingress_job_id

    def Integration_SubProc(self):
        self.service.INTEGRATION_HOME = self.service.meshClient.INTEGRATION_HOME + "/outputs"
        self.service.integration_cache_subproc(
            self.service.INGRESS_DATA_HOME,
            self.service.INTEGRATION_INPUT_CACHE
        )
        wait_for_directory(self.service.INTEGRATION_INPUT_CACHE, check_interval=1)
        self.integrated_subproc(self.service.INTEGRATION_INPUT_DATA_CACHE, self.service.INTEGRATION_HOME)
        wait_for_directory(self.service.INTEGRATION_HOME, check_interval=1)
        self.integration_output = self.service.meshClient.cidDir(self.service.INTEGRATION_HOME)
        self.integration_output_ipfs = f'ipfs://{self.integration_output}/*.csv'
        return self.integration_output

    def Egress_SubProc(self):
        self.egress_job_id = self.egress_subproc(input_dir=self.integration_output_ipfs)
        self.service.EGRESS_JOB_STATUS = self.service.meshClient.waitForJobCompletion(
            self.egress_job_id, check_interval=1, timeout=None
        )
        published_results = self.service.meshClient.getPublishedURI(self.egress_job_id)
        self.invoice_data_cid = published_results['CID']
        self.service.meshClient.EGRESS_HOME = self.invoice_data_cid
        self.service.EGRESS_EXIT_CODE = self.service.meshClient.cat(self.service.meshClient.EGRESS_HOME + "/exitCode")
        self.service.EGRESS_HOME = f'ipfs://{self.service.meshClient.EGRESS_HOME}/outputs'
        return self.egress_job_id

    def process(self):
        print("CAT Executing")
        self.ingress_job_id = self.Ingress_SubProc()
        self.integration_output = self.Integration_SubProc()
        self.egress_job_id = self.Egress_SubProc()
        print("...")
        print(self.ingress_job_id)
        print(self.integration_output)
        print(self.egress_job_id)
        print("CAT Executed")
        return self.ingress_job_id, self.integration_output, self.egress_job_id