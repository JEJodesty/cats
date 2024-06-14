from cats.executor.function import InfraFunction, Processor
from cats.executor.structure import InfraStructure


class Structure:
    def __init__(self, service):
        self.service = service
        self.bom_json_cid = self.service.bom_json_cid
        # self.plant: Plant = plant
        self.infraStructure: InfraStructure = InfraStructure(service=self.service)

    def redeploy(self):
        print()
        print()
        print('Deploy Structure!')
        self.infraStructure.destroy()
        self.infraStructure.initialize()
        self.infraStructure.apply()



class Function:
    def __init__(self, service):
        self.service = service
        self.CAT_HOME = None
        self.processor: Processor = Processor(service=self.service)
        self.ingress_job_id = None
        self.integration_output = None
        self.egress_job_id = None
        self.invoice_data_cid = None

    def execute(self):
        self.ingress_job_id, self.integration_output, self.egress_job_id = self.processor.process()
        self.invoice_data_cid = self.processor.invoice_data_cid
        return self.ingress_job_id, self.integration_output, self.egress_job_id