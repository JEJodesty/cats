import json
from cats.io.input.structure import Structure
from cats.io.input.function import Function


class Executor:
    def __init__(self,
        service
    ):
        self.service = service
        self.CAT_HOME = self.service.CAT_HOME

        self.structure: Structure = Structure(self.service)
        self.function: Function = Function(self.service)
        self.bom_json_cid: str = self.service.bom_json_cid
        self.enhanced_bom, self.bom = self.service.meshClient.getEnhancedBom(
            self.bom_json_cid, self.service.DATA_HOME
        )
        self.orderCID = None
        self.invoiceCID = None

        self.ingress_job_id = None
        self.integration_s3_output = None
        self.egress_job_id = None


    def execute(self, enhanced_bom=None):
        if enhanced_bom is not None:
            self.enhanced_bom = enhanced_bom

        self.invoiceCID = self.enhanced_bom['invoice_cid']
        self.orderCID = self.enhanced_bom['invoice']['order_cid']

        self.structure.redeploy()
        self.ingress_job_id, self.integration_s3_output, self.egress_job_id = self.function.execute()

        self.enhanced_bom['function'] = json.loads(self.service.meshClient.cat(self.enhanced_bom['order']['function_cid']))
        self.enhanced_bom['log'] = {
            'ingress_job_id': self.ingress_job_id,
            'integration_output': self.integration_s3_output,
            'egress_job_id': self.egress_job_id
        }
        self.enhanced_bom['invoice']['data_cid'] = self.function.invoice_data_cid
        self.enhanced_bom['log_cid'] = self.service.ipfsClient.add_json(self.enhanced_bom['log'])

        del self.enhanced_bom['bom_json_cid']
        del self.enhanced_bom['init_data_cid']
        #
        # print(os.getcwd())
        # exit()

        # os.remove("bom.json")
        # os.remove("invoice.json")
        # os.remove("order.json")
        # os.remove("bom.car")
        # os.remove("cat-action-plane-config")
        return self.enhanced_bom, None
        # return self.invoiceCID
