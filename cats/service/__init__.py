import glob, json, os, pickle
from pathlib import Path
import pandas as pd
import ipfsapi as ipfsApi
import boto3 as boto3

from cats.factory import Factory
from cats.service.utils import executeCMD
from cats.network import MeshClient


class Service:
    def __init__(self,
        meshClient: MeshClient,
        CATS_HOME: str
    ):
        self.meshClient: MeshClient = meshClient
        self.ipfsClient: ipfsApi = self.meshClient.ipfsClient
        self.executeCMD = executeCMD

        self.AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID'),
        self.AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.S3_CLIENT = boto3.client(
            's3',
            region_name='us-east-2',
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY
        )
        self.CATS_HOME = self.meshClient.CATS_HOME = CATS_HOME
        self.DATA_HOME = self.meshClient.DATA_HOME = self.CATS_HOME + '/data'
        self.JOB_HOME = self.meshClient.JOB_HOME = self.DATA_HOME + '/jobs'
        self.CACHE_HOME = self.meshClient.CACHE_HOME = self.DATA_HOME + "/cache"
        self.INPUT_HOME = self.meshClient.INPUT_HOME = self.DATA_HOME + '/input'
        self.OUTPUT_HOME = self.meshClient.OUTPUT_HOME = self.DATA_HOME + '/output'
        self.INTEGRATION_INPUT_CACHE = self.meshClient.INTEGRATION_INPUT_CACHE = \
            f"{self.CACHE_HOME}/integration"
        self.INTEGRATION_INPUT_DATA_CACHE = self.meshClient.INTEGRATION_INPUT_DATA_CACHE = \
            f"{self.INTEGRATION_INPUT_CACHE}/outputs"
        self.bucket_name = self.DATA_HOME.split('/')[-1]
        self.job_directory_path = f"{self.JOB_HOME.split('/')[-1]}/"
        self.cache_directory_path = f"{self.CACHE_HOME.split('/')[-1]}/"
        self.catStore()

        self.CAT_HOME = None
        self.INGRESS_HOME = None
        self.INGRESS_DATA_HOME = None
        self.INGRESS_EXIT_CODE = None
        self.INGRESS_JOB_STATUS = None
        self.INTEGRATION_HOME = None
        self.EGRESS_HOME = None
        self.EGRESS_EXIT_CODE = None
        self.EGRESS_JOB_STATUS = None

        self.init_bom_json_cid = None
        self.bom_json_cid = None
        self.init_bom_car_cid = None
        self.enhanced_init_bom = None
        self.enhanced_bom = None

        self.ingress_subproc_cid = None
        self.integrated_subproc_cid = None
        self.egress_subproc_cid = None
        self.integration_cache_subproc_cid = None

        self.ingress_subproc = None
        self.integrated_subproc = None
        self.egress_subproc = None
        self.integration_cache_subproc = None

        self.orderCID = None
        self.dataCID = None
        self.functionCID = None
        self.order = None
        self.process = None

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

    def catStore(self):
        Path(self.DATA_HOME).mkdir(parents=True, exist_ok=True)
        Path(self.JOB_HOME).mkdir(parents=True, exist_ok=True)
        Path(self.CACHE_HOME).mkdir(parents=True, exist_ok=True)
        Path(self.INPUT_HOME).mkdir(parents=True, exist_ok=True)
        Path(self.OUTPUT_HOME).mkdir(parents=True, exist_ok=True)

    def initFactory(self, order_request, ipfs_uri):
        self.initBOMcar(
            structure_cid=order_request['order']['structure_cid'],
            structure_filepath=order_request['order']['structure_filepath'],
            function_cid=order_request['order']['function_cid'],
            init_data_cid=ipfs_uri,
            init_bom_filename=f"{self.OUTPUT_HOME}/bom.car"
        )
        catFactory = Factory(self)
        return catFactory, order_request

    def execute(self, catFactory, order_request):
        executor = catFactory.produce()
        enhanced_bom, _ = executor.execute()

        invoice = {}
        enhanced_bom['invoice']['order_cid'] = self.ipfsClient.add_str(
            json.dumps(order_request['order'])
        )
        invoice['invoice_cid'] = self.ipfsClient.add_str(
            json.dumps(enhanced_bom['invoice'])
        )
        invoice['invoice'] = enhanced_bom['invoice']

        bom = {
            'log_cid': enhanced_bom['log_cid'],
            'invoice_cid': invoice['invoice_cid']
        }
        bom_response = {
            'bom': bom,
            'bom_cid': self.ipfsClient.add_str(json.dumps(bom))
        }
        return bom_response

    def cid_to_pandasDF(self, cid, download_dir, format='*.csv', read_dir='/outputs', parrent_dir=None):
        if parrent_dir is None:
            parrent_dir = self.CATS_HOME

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
        function_cid, init_data_cid, init_bom_filename,
        structure_cid=None, structure_filepath=None
    ):
        if init_bom_filename is None:
            init_bom_filename = self.meshClient.CAR_HOME

        self.init_bom_car_cid, self.init_bom_json_cid = self.meshClient.initBOMcar(
            structure_cid=structure_cid,
            structure_filepath=structure_filepath,
            function_cid=function_cid,
            init_data_cid=init_data_cid,
            init_bom_filename=init_bom_filename
        )
        self.enhanced_bom, init_bom = self.meshClient.getEnhancedBom(
            bom_json_cid=self.init_bom_json_cid,
            INPUT_HOME=self.INPUT_HOME,
            OUTPUT_HOME=self.OUTPUT_HOME
        )
        self.functionCID = self.enhanced_bom['order']['function_cid']
        function_dict = json.loads(self.meshClient.cat(self.functionCID))
        self.ingress_subproc_cid = function_dict['ingress_subproc_cid']
        self.integrated_subproc_cid = function_dict['integrated_subproc_cid']
        self.egress_subproc_cid = function_dict['egress_subproc_cid']
        self.integration_cache_subproc_cid = function_dict['integration_cache_subproc_cid']

        self.ingress_subproc = pickle.loads(self.meshClient.catObj(self.ingress_subproc_cid))
        self.integrated_subproc = pickle.loads(self.meshClient.catObj(self.integrated_subproc_cid))
        self.egress_subproc = pickle.loads(self.meshClient.catObj(self.egress_subproc_cid))
        self.integration_cache_subproc = pickle.loads(self.meshClient.catObj(self.integration_cache_subproc_cid))

        self.order_cid = self.enhanced_bom['invoice']['order_cid']
        self.init_bom_json_cid = self.enhanced_bom['bom_json_cid']
        self.bom_json_cid = self.init_bom_json_cid
        return self.init_bom_car_cid, self.init_bom_json_cid

    # def catSubmit(self, bom):
    #     order = json.loads(self.meshClient.cat(bom["order_cid"]))
    #     print("Order:")
    #     print()
    #     pprint(order)
    #     print()
    #     ppost = lambda args, endpoint: \
    #         f'curl -X POST -H "Content-Type: application/json" -d \\\n\'{json.dumps(**args)}\' {endpoint}'
    #     post = lambda args, endpoint: \
    #         'curl -X POST -H "Content-Type: application/json" -d \'' + json.dumps(**args) + f'\' {endpoint}'
    #
    #     post_cmd = post({'obj': bom}, order["endpoint"])
    #     print(ppost({'obj': bom, 'indent': 4}, order["endpoint"]))
    #     print()
    #     response_str = subprocess.check_output(post_cmd, shell=True)
    #     output_bom = json.loads(response_str)
    #
    #     output_bom['POST'] = post_cmd
    #     return output_bom

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
