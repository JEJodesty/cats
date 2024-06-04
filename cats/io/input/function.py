from datetime import datetime, time
from pathlib import Path
from ray.data import Dataset
from cats.utils import wait_for_directory


class IO:
    def __init__(self, reader, writer):
        self.processor: Processor = None
        self.input, self.output = None, None
        self.function = None
        self.Reader = reader
        self.Writer = writer
        self.ds_in: Dataset = None
        self.ds_out: Dataset = None

    def read(self):
        self.input = self.processor.ingress_input
        self.ds_in = self.Reader(self.input)

    def write(self):
        self.output = self.processor.integration_output
        self.Writer(self.ds_out, self.output)

    def transform(self, processor):
        self.processor = processor
        self.read()
        self.ds_out = self.processor.process(self.ds_in)
        print(self.ds_out.show(limit=1))
        self.write()
        return self.ds_out

    def view(self, processor):
        self.processor = processor
        self.read()
        self.ds_out = self.processor.process(self.ds_in)
        self.write()
        return self.ds_out


class Processor:
    def __init__(self, service):
        self.service = service
        self.processCID = self.service.processCID

        self.process = self.service.process
        self.ingress = self.service.meshClient.ingress
        self.integration = self.service.meshClient.integrationDownload
        self.egress = self.service.meshClient.egress

        self.ingress_input_data_cid = self.service.enhanced_bom['init_data_cid']
        # self.ingress_input_data_cid = self.service.enhanced_bom['invoice']['data_cid']
        self.integrated_data_cid = None
        self.outDataCID = None
        self.seedCID = None

        self.ds_in = None
        self.ds_out = None

        self.ingress_job_id = None
        self.ingress_input = None
        self.ingress_output = None

        # self.ingressed_data_cid = None
        # self.ingress_job_dir = None
        self.integration_output = None
        self.integration_output_ipfs = None
        # self.integration_job_id = None
        self.egress_output = None
        self.egress_job_id = None
        self.egressed_data_cid = None

        self.invoice_data_dir = None
        self.invoice_data_cid = None

    def Ingress_SubProc(self):
        self.ingress_job_id = self.ingress(input_dir=self.ingress_input_data_cid)
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
        self.integration(
            self.service.INGRESS_DATA_HOME,
            self.service.INTEGRATION_INPUT_CACHE
        )
        wait_for_directory(self.service.INTEGRATION_INPUT_CACHE, check_interval=1)
        self.process(self.service.INTEGRATION_INPUT_DATA_CACHE, self.service.INTEGRATION_HOME)
        wait_for_directory(self.service.INTEGRATION_HOME)
        self.integration_output = self.service.meshClient.cidDir(self.service.INTEGRATION_HOME)
        self.integration_output_ipfs = f'ipfs://{self.integration_output}/*.csv'
        return self.integration_output

    def Egress_SubProc(self):
        self.egress_job_id = self.egress(input_dir=self.integration_output_ipfs)
        self.service.EGRESS_JOB_STATUS = self.service.meshClient.waitForJobCompletion(
            self.egress_job_id, check_interval=1, timeout=None
        )
        published_results = self.service.meshClient.getPublishedURI(self.egress_job_id)
        self.invoice_data_cid = published_results['CID']
        self.service.meshClient.EGRESS_HOME = self.invoice_data_cid
        self.service.EGRESS_EXIT_CODE = self.service.meshClient.cat(self.service.meshClient.EGRESS_HOME + "/exitCode")
        self.service.EGRESS_HOME = f'ipfs://{self.service.meshClient.EGRESS_HOME}/outputs'
        return self.egress_job_id

    def execute(self):
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


class InfraFunction(Processor):
    def __init__(self, service):
        self.service = service
        # self.infrafunctionCID = self.service.infrafunctionCID
        self.process: Processor = Processor(self.service)


class Function(InfraFunction):
    def __init__(self, service):
        self.CAT_HOME = None
        self.service = service

        self.infraFunction: InfraFunction = InfraFunction(self.service)
        self.processor: Processor = self.infraFunction.process
        self.process = self.service.process
        self.ingress_job_id = None
        self.integration_s3_output = None
        self.egress_job_id = None
        self.invoice_data_cid = None

    def catStore(self):
        self.CAT_HOME = self.service.meshClient.CAT_HOME = f"""{self.service.JOB_HOME}/cat={datetime.utcnow().isoformat()}"""
        self.service.INGRESS_HOME = self.service.meshClient.INGRESS_HOME = f"{self.CAT_HOME}/ingress"
        self.service.INTEGRATION_HOME = self.service.meshClient.INTEGRATION_HOME = f"{self.CAT_HOME}/integration"
        self.service.EGRESS_HOME = self.service.meshClient.EGRESS_HOME = f"{self.CAT_HOME}/egress"
        self.service.PROCESSES_HOME = self.service.meshClient.PROCESSES_HOME = f"{self.CAT_HOME}/process"

        Path(self.service.INGRESS_HOME).mkdir(parents=True, exist_ok=True)
        Path(self.service.INTEGRATION_HOME).mkdir(parents=True, exist_ok=True)
        Path(self.service.INTEGRATION_INPUT_CACHE).mkdir(parents=True, exist_ok=True)
        Path(self.service.PROCESSES_HOME).mkdir(parents=True, exist_ok=True)

    def execute(self):
        self.catStore()
        self.ingress_job_id, self.integration_s3_output, self.egress_job_id = self.processor.execute()
        self.invoice_data_cid = self.processor.invoice_data_cid
        return self.ingress_job_id, self.integration_s3_output, self.egress_job_id