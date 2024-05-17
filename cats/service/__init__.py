import glob, json, os, pickle, subprocess
from copy import deepcopy
from pprint import pprint
import pandas as pd

from cats import CATS_HOME
from cats.service.utils import executeCMD
from cats.network import MeshClient
import ipfsapi as ipfsApi

class Service:
    def __init__(self,
        meshClient: MeshClient
    ):
        self.meshClient: MeshClient = meshClient
        self.ipfsClient: ipfsApi = self.meshClient.ipfsClient
        self.executeCMD = executeCMD
        self.CAR_HOME = self.meshClient.CAT_HOME + '/bom.car'

        self.init_bom_json_cid = None
        self.bom_json_cid = None
        self.init_bom_car_cid = None
        self.enhanced_init_bom = None
        self.enhanced_bom = None
        # self.enhanced_init_bom = None

        self.ingress_subproc_cid = None
        self.integration_subproc_cid = None
        self.egress_subproc_cid = None

        self.ingress_subproc = None
        self.integration_subproc = None
        self.egress_subproc = None

        self.orderCID = None
        self.dataCID = None
        self.functionCID = None
        self.processCID = None
        self.order = None
        self.process = None
    #     self.start_ipfs_daemon
    #
    # def start_ipfs_daemon(self):
    #     # Command to start the IPFS daemon
    #     command = ['ipfs', 'daemon']
    #
    #     # Start the daemon
    #     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #
    #     # You can now handle the output or errors if necessary
    #     stdout, stderr = process.communicate()
    #
    #     if process.returncode == 0:
    #         print("IPFS daemon started successfully.")
    #         print(stdout.decode())
    #     else:
    #         print("Failed to start IPFS daemon.")
    #         print(stderr.decode())

    def cid_to_pandasDF(self, cid, download_dir, format='*.csv', read_dir='/outputs', parrent_dir=CATS_HOME):
        path = f'{parrent_dir}/{download_dir}'
        os.system(f"rm -rf {path}")
        self.meshClient.get(cid, download_dir, parrent_dir)

        # Get the files from the path provided
        files = glob.glob(os.path.join(f"{path}{read_dir}", format))
        dfs = list(pd.read_csv(f).assign(filename=f) for f in files)
        df = None
        for dfx in dfs:
            if df is None:
                df = dfx
            else:
                df = pd.concat([df, dfx], ignore_index=True)
        return df

    def initBOMcar(self,
        function_cid, init_data_cid, init_bom_filename=None,
        structure_cid=None, structure_filepath=None
    ):
        if init_bom_filename is None:
            init_bom_filename = self.CAR_HOME

        self.init_bom_car_cid, self.init_bom_json_cid = self.meshClient.initBOMcar(
            # structure_path=self.MeshClient.g,
            structure_cid=structure_cid,
            structure_filepath=structure_filepath,
            function_cid=function_cid,
            init_data_cid=init_data_cid,
            init_bom_filename=init_bom_filename
        )
        self.enhanced_bom, init_bom = self.meshClient.getEnhancedBom(bom_json_cid=self.init_bom_json_cid)

        self.functionCID = self.enhanced_bom['order']['function_cid']
        function_dict = json.loads(self.meshClient.cat(self.functionCID))
        self.processCID = function_dict['process_cid']
        self.process = pickle.loads(self.meshClient.catObj(self.processCID))

        self.order_cid = self.enhanced_bom['invoice']['order_cid']
        self.init_bom_json_cid = self.enhanced_bom['bom_json_cid']
        self.bom_json_cid = self.init_bom_json_cid
        return self.init_bom_car_cid, self.init_bom_json_cid

    def catSubmit(self, bom):
        order = json.loads(self.meshClient.cat(bom["order_cid"]))
        print("Order:")
        print()
        pprint(order)
        print()
        print()

        ppost = lambda args, endpoint: \
            f'curl -X POST -H "Content-Type: application/json" -d \\\n\'{json.dumps(**args)}\' {endpoint}'
        post = lambda args, endpoint: \
            'curl -X POST -H "Content-Type: application/json" -d \'' + json.dumps(**args) + f'\' {endpoint}'

        post_cmd = post({'obj': bom}, order["endpoint"])
        print(ppost({'obj': bom, 'indent': 4}, order["endpoint"]))
        print()
        print()
        response_str = subprocess.check_output(post_cmd, shell=True)
        output_bom = json.loads(response_str)

        output_bom['POST'] = post_cmd
        return output_bom

    def flatten_bom(self, bom_response):
        invoice = json.loads(
            self.meshClient.cat(bom_response["bom"]["invoice_cid"])
        )
        invoice['order'] = json.loads(
            self.meshClient.cat(invoice['order_cid']),
        )
        invoice['order']['flat'] = {
            'function': json.loads(self.meshClient.cat(invoice['order']["function_cid"])),
            'invoice': json.loads(self.meshClient.cat(invoice['order']["invoice_cid"]))
        }
        bom_response["flat_bom"] = {
            'invoice': invoice,
            'log': json.loads(
                self.meshClient.cat(bom_response["bom"]["log_cid"])
            )
        }
        return bom_response

    def create_order_request(self,
        process_obj, data_dirpath, structure_filepath,
        endpoint='http://127.0.0.1:5000/cat/node/execute'
    ):
        structure_cid, structure_name = self.meshClient.cidFile(structure_filepath)
        function = {
            'process_cid': self.ipfsClient.add_pyobj(process_obj),
            'infrafunction_cid': None
        }
        invoice = {
            "data_cid": self.meshClient.cidDir(data_dirpath)
        }
        order = {
            "function_cid": self.ipfsClient.add_str(json.dumps(function)),
            "structure_cid": structure_cid,
            "invoice_cid": self.ipfsClient.add_str(json.dumps(invoice)),
            "structure_filepath": structure_name,
            "endpoint": endpoint
        }
        self.order = {
            'order_cid': self.ipfsClient.add_str(json.dumps(order))
        }
        return self.order

    def linkProcess(self, cat_response, process_obj):
        flattened_bom = self.flatten_bom(cat_response)
        flat_bom = deepcopy(flattened_bom['flat_bom'])

        function = {
            'process_cid': self.ipfsClient.add_pyobj(process_obj),
            'infrafunction': None
        }

        invoice = flat_bom['invoice']
        input_invoice = {'data_cid': invoice['data_cid']}
        new_function_cid = self.ipfsClient.add_str(json.dumps(function))
        new_invoice_cid = self.ipfsClient.add_str(json.dumps(input_invoice))

        order = invoice['order']
        order['function_cid'] = new_function_cid
        order['invoice_cid'] = new_invoice_cid
        del order['flat']
        order['endpoint'] = 'http://127.0.0.1:5000/cat/node/link'

        order_request = {'order_cid': self.ipfsClient.add_str(json.dumps(order))}
        return order_request
