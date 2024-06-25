import json, pickle
from cats.utils import wait_for_directory


class Processor:
    def __init__(self, infraFunction):
        self.infraFunction = infraFunction
        self.invoice_data_cid = None

        self.ingress_job_id = None
        self.ingress_input_data_cid = self.infraFunction.enhanced_bom['init_data_cid']
        self.integration_output = None
        self.integration_output_ipfs = None
        self.egress_job_id = None

    def Ingress(self):
        self.ingress_job_id = self.infraFunction.ingress_subproc(input_dir=self.ingress_input_data_cid)
        self.infraFunction.service.INGRESS_JOB_STATUS = \
            self.infraFunction.service.meshClient.waitForJobCompletion(
                self.ingress_job_id, check_interval=1, timeout=None
            )
        published_results = self.infraFunction.service.meshClient.getPublishedURI(self.ingress_job_id)
        self.infraFunction.service.meshClient.INGRESS_HOME = published_results['Params']['CID']
        self.infraFunction.service.INGRESS_EXIT_CODE = self.infraFunction.service.meshClient.cat(
            self.infraFunction.service.meshClient.INGRESS_HOME + "/exitCode"
        )
        self.infraFunction.service.INGRESS_DATA_HOME = \
            f'ipfs://{self.infraFunction.service.meshClient.INGRESS_HOME}/outputs'
        return self.ingress_job_id

    def Integration(self):
        self.infraFunction.service.INTEGRATION_HOME = \
            self.infraFunction.service.meshClient.INTEGRATION_HOME + "/outputs"
        self.infraFunction.integration_cache_subproc(
            self.infraFunction.service.INGRESS_DATA_HOME,
            self.infraFunction.service.INTEGRATION_INPUT_CACHE
        )
        wait_for_directory(self.infraFunction.service.INTEGRATION_INPUT_CACHE, check_interval=1)
        self.infraFunction.integrated_subproc(
            self.infraFunction.service.INTEGRATION_INPUT_DATA_CACHE,
            self.infraFunction.service.INTEGRATION_HOME
        )
        wait_for_directory(self.infraFunction.service.INTEGRATION_HOME, check_interval=1)
        self.integration_output = \
            self.infraFunction.service.meshClient.cidDir(self.infraFunction.service.INTEGRATION_HOME)
        self.integration_output_ipfs = f'ipfs://{self.integration_output}/*.csv'
        return self.integration_output

    def Egress(self):
        self.egress_job_id = self.infraFunction.egress_subproc(input_dir=self.integration_output_ipfs)
        self.infraFunction.service.EGRESS_JOB_STATUS = \
            self.infraFunction.service.meshClient.waitForJobCompletion(
                self.egress_job_id, check_interval=1, timeout=None
            )
        published_results = self.infraFunction.service.meshClient.getPublishedURI(self.egress_job_id)
        self.infraFunction.service.meshClient.EGRESS_HOME = self.invoice_data_cid = published_results['Params']['CID']
        self.infraFunction.service.EGRESS_EXIT_CODE = self.infraFunction.service.meshClient.cat(
            self.infraFunction.service.meshClient.EGRESS_HOME + "/exitCode"
        )
        self.infraFunction.service.EGRESS_HOME = \
            f'ipfs://{self.infraFunction.service.meshClient.EGRESS_HOME}/outputs'
        return self.egress_job_id

    def process(self):
        print("CAT Executing")
        self.ingress_job_id = self.Ingress()
        self.integration_output = self.Integration()
        self.egress_job_id = self.Egress()
        print("...")
        print(self.ingress_job_id)
        print(self.integration_output)
        print(self.egress_job_id)
        print("CAT Executed")
        return self.ingress_job_id, self.integration_output, self.egress_job_id


class InfraFunction:
    def __init__(self, service):
        self.service = service
        self.enhanced_bom = self.service.enhanced_bom
        self.function_cid = self.enhanced_bom['order']['function_cid']
        self.function = json.loads(self.service.meshClient.cat(self.function_cid))
        self.ingress_subproc_cid = self.function['ingress_subproc_cid']
        self.integrated_subproc_cid = self.function['integrated_subproc_cid']
        self.egress_subproc_cid = self.function['egress_subproc_cid']
        self.integration_cache_subproc_cid = self.function['integration_cache_subproc_cid']

        self.ingress_subproc = pickle.loads(self.service.meshClient.catObj(self.ingress_subproc_cid))
        self.integrated_subproc = pickle.loads(self.service.meshClient.catObj(self.integrated_subproc_cid))
        self.egress_subproc = pickle.loads(self.service.meshClient.catObj(self.egress_subproc_cid))
        self.integration_cache_subproc = pickle.loads(
            self.service.meshClient.catObj(self.integration_cache_subproc_cid)
        )

    def compose(self):
        return Processor(self)


