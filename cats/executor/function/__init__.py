import json, pickle
from pathlib import Path
from pprint import pprint

from cats.utils import wait_for_directory


class Processor:
    def __init__(self, infraFunction):
        self.infraFunction = infraFunction
        self.invoice_data_cid = None

        self.ingress_input_data_cid = self.infraFunction.enhanced_bom['init_data_cid']
        self.ingress_data_cid = None
        self.integration_data_cid = None
        self.egress_data_cid = None

    def Ingress(self):
        self.infraFunction.service.INGRESS_DATA_HOME = self.ingress_data_cid = \
            self.infraFunction.ingress_subproc(input_dir_cid=self.ingress_input_data_cid)
        self.infraFunction.service.INGRESS_JOB_STATUS = "Completed"
        self.infraFunction.service.INGRESS_EXIT_CODE = "0"
        return self.ingress_data_cid

    def Integration(self):
        self.infraFunction.service.INTEGRATION_HOME = \
            self.infraFunction.service.meshClient.INTEGRATION_HOME + "/outputs"
        # Path(self.infraFunction.service.INTEGRATION_INPUT_CACHE).mkdir(parents=True, exist_ok=True)
        # Path(self.infraFunction.service.INTEGRATION_INPUT_DATA_CACHE).mkdir(parents=True, exist_ok=True)
        self.infraFunction.integration_cache_subproc(
            input_dir_cid=self.infraFunction.service.INGRESS_DATA_HOME,
            cwd=self.infraFunction.service.INTEGRATION_INPUT_CACHE
            # cwd=self.infraFunction.service.INTEGRATION_INPUT_DATA_CACHE
            # v_output_dir=self.infraFunction.service.INTEGRATION_INPUT_DATA_CACHE
        )
        wait_for_directory(self.infraFunction.service.INTEGRATION_INPUT_DATA_CACHE, check_interval=1)
        self.infraFunction.integrated_subproc(
            self.infraFunction.service.INTEGRATION_INPUT_DATA_CACHE,
            self.infraFunction.service.INTEGRATION_HOME
        )
        wait_for_directory(self.infraFunction.service.INTEGRATION_HOME, check_interval=1)
        self.integration_data_cid, _ = \
            self.infraFunction.service.meshClient.cidDir(self.infraFunction.service.INTEGRATION_HOME)
        # print(self.infraFunction.service.INGRESS_DATA_HOME)
        # print(self.infraFunction.service.INTEGRATION_INPUT_DATA_CACHE)
        # print(self.infraFunction.service.INTEGRATION_HOME)
        # print(self.integration_data_cid)
        # exit()
        return self.integration_data_cid

    def Egress(self):
        self.infraFunction.service.meshClient.EGRESS_HOME = \
            self.egress_data_cid = self.invoice_data_cid = \
            self.infraFunction.egress_subproc(
                input_dir_cid=self.integration_data_cid
            )
        self.infraFunction.service.EGRESS_JOB_STATUS = "Completed"
        self.infraFunction.service.EGRESS_EXIT_CODE = "0"
        return self.egress_data_cid

    def process(self):
        print("CAT Executing")
        self.ingress_data_cid = self.Ingress()
        self.integration_data_cid = self.Integration()
        self.egress_data_cid = self.Egress()
        print("...")
        print(self.ingress_data_cid)
        print(self.integration_data_cid)
        print(self.egress_data_cid)
        print("CAT Executed")
        return self.ingress_data_cid, self.integration_data_cid, self.egress_data_cid


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


