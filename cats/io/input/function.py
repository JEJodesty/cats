from ray.data import Dataset
from cats.service import Service
import datetime


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
    def __init__(self, service: Service):
        self.service = service
        self.processCID = self.service.processCID
        self.process = self.service.process
        self.inDataCID = self.service.enhanced_bom['init_data_cid']
        # self.inDataCID = self.service.enhanced_bom['invoice']['data_cid']
        self.integratedDataCID = None
        self.outDataCID = None
        self.seedCID = None

        self.ds_in = None
        self.ds_out = None

        self.ingress_job_id = None
        self.ingress_input = None
        # self.ingress_job_dir = None
        self.integration_output = None
        self.integration_output_ipfs_dir = None
        # self.integration_job_id = None
        self.egress_job_id = None
        self.invoice_data_dir = None
        self.invoice_data_cid = None

    def cidDirUponCompletion(self, data_dir, job_id):
        status = self.service.meshClient.checkStatusOfJob(job_id=job_id)
        if status == "Completed":
            data_dir_cid = self.service.meshClient.cidDir(data_dir)
            return data_dir_cid
        else:
            return self.cidDirUponCompletion(data_dir)

    def Ingress(self):
        self.ingress_job_id = self.service.meshClient.ingress(input=self.inDataCID)
        # self.ingress_job_id.split('/job-')
        # print(self.ingress_job_id)
        # exit()
        # r = self.service.meshClient.checkStatusOfJob(job_id=self.ingress_job_id)
        return self.ingress_job_id

    def Integration(self):
        self.ingress_input = self.service.meshClient.integrate(self.ingress_job_id)
        self.integration_output = self.service.meshClient.CAT_HOME + '/integration/outputs'
        self.process(self.ingress_input, self.integration_output + "/")
        self.integratedDataCID = self.service.meshClient.cidDir(self.integration_output)
        self.integration_output_ipfs_dir = f'ipfs://{self.integratedDataCID}'
        return self.integration_output

    def Egress(self):
        self.egress_job_id, self.invoice_data_dir = self.service.meshClient.egress(
            integration_output_cid=self.integration_output_ipfs_dir
        )
        # print(self.invoice_data_dir)
        # print(type(self.invoice_data_dir))
        self.invoice_data_cid = self.cidDirUponCompletion(self.invoice_data_dir, self.egress_job_id)
        # print(self.invoice_data_cid)
        # exit()
        return self.egress_job_id

    def execute(self):
        self.ingress_job_id = self.Ingress()
        self.integration_output = self.Integration()
        self.egress_job_id = self.Egress()
        return self.ingress_job_id, self.integration_output, self.egress_job_id


class InfraFunction(Processor):
    def __init__(self, service: Service):
        self.service = service
        # self.infrafunctionCID = self.service.infrafunctionCID
        self.process: Processor = Processor(self.service)


class Function(InfraFunction):
    def __init__(self, service: Service):
        self.service: Service = service
        self.infraFunction: InfraFunction = InfraFunction(self.service)
        self.processor: Processor = self.infraFunction.process
        self.process = self.service.process
        self.ingress_job_id = None
        self.integration_s3_output = None
        self.egress_job_id = None
        self.invoice_data_cid = None

    def execute(self):
        self.ingress_job_id, self.integration_s3_output, self.egress_job_id = self.processor.execute()
        self.invoice_data_cid = self.processor.invoice_data_cid
        return self.ingress_job_id, self.integration_s3_output, self.egress_job_id