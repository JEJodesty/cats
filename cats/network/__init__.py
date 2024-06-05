import json, subprocess
from copy import copy, deepcopy
from cats.network.cod import CoD


class MeshClient(CoD):
    def __init__(self, ipfsClient, filecoinClient=None, awsClient=None):
        self.CATS_HOME = None
        self.DATA_HOME = None
        self.JOB_HOME = None
        self.CACHE_HOME = None

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

    def getEnhancedBom(self, bom_json_cid: str, CAT_HOME: str):
        # self.get(cid=bom_json_cid, filepath='bom.json', cwd=None)
        # bom = json.loads(open('bom.json', 'r').read())
        # self.CAT_HOME = CAT_HOME
        self.CAR_HOME = self.DATA_HOME + '/bom.car'
        self.get(cid=bom_json_cid, output=self.DATA_HOME, filepath='bom.json')
        bom = json.loads(open(f'{self.DATA_HOME}/bom.json', 'r').read())
        enhanced_bom = deepcopy(bom)
        enhanced_bom['bom_json_cid'] = bom_json_cid

        self.get(cid=bom['invoice_cid'], output=self.DATA_HOME, filepath='invoice.json')
        enhanced_bom['invoice'] = json.loads(open(f'{self.DATA_HOME}/invoice.json', 'r').read())

        self.get(cid=enhanced_bom['invoice']['order_cid'],
                 output=self.DATA_HOME, filepath='order.json')
        enhanced_bom['order'] = json.loads(open(f'{self.DATA_HOME}/order.json', 'r').read())

        self.get(
            cid=enhanced_bom['order']['structure_cid'], output=self.DATA_HOME,
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
        # # data_dir = filepath.split('/')[-1]
        # print('0')
        # print(filepath)
        # print('1')
        # print(data)
        # # print('2')
        # # print(data_dir)
        # # print('3')
        # # print(list(filter(lambda x: x['Name'] == data_dir, data)))
        # exit()
        if type(data) is list:
            data_json = list(filter(lambda x: x['Name'] == 'outputs', data))[-1]
            data_cid = data_json['Hash']
            return data_cid
        else:
            data_json = data
            data_cid = data_json['Hash']
            return data_cid