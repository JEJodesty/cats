import json
from pprint import pprint

import ipfsapi as ipfsApi
from cats.network import MeshClient
from cats.service import Service
from cats.factory import Factory
from flask import Flask, request, jsonify

cat = Flask(__name__)

node_service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)


def initFactory(order_request, ipfs_uri):
    # if cod_out is False:
    #     ipfs_uri = f'ipfs://{order_request["invoice"]["data_cid"]}/*csv'
    # elif cod_out is True:
    #     ipfs_uri = f'ipfs://{order_request["invoice"]["data_cid"]}/output/*csv'
    node_service.initBOMcar(
        structure_cid=order_request['order']['structure_cid'],
        structure_filepath=order_request['order']['structure_filepath'],
        function_cid=order_request['order']['function_cid'],
        init_data_cid=ipfs_uri
    )
    catFactory = Factory(node_service)
    return catFactory, order_request


def execute(catFactory, order_request):
    executor = catFactory.produce()
    enhanced_bom, _ = executor.execute()

    invoice = {}
    enhanced_bom['invoice']['order_cid'] = node_service.ipfsClient.add_str(
        json.dumps(order_request['order'])
    )
    invoice['invoice_cid'] = node_service.ipfsClient.add_str(
        json.dumps(enhanced_bom['invoice'])
    )
    invoice['invoice'] = enhanced_bom['invoice']

    bom = {
        'log_cid': enhanced_bom['log_cid'],
        'invoice_cid': invoice['invoice_cid']
    }
    bom_response = {
        'bom': bom,
        'bom_cid': node_service.ipfsClient.add_str(json.dumps(bom))
    }
    return bom_response


order_request = {'order_cid': 'QmNU5EAmWNDc7U3bjZ8X2rzjD3iN83KXcarsvnyk8AXA9o'}
order_request["order"] = json.loads(node_service.meshClient.cat(order_request["order_cid"]))
order_request['invoice'] = json.loads(node_service.meshClient.cat(order_request['order']['invoice_cid']))

ipfs_uri = f'ipfs://{order_request["invoice"]["data_cid"]}/*.csv'
catFactory, updated_order_request = initFactory(order_request, ipfs_uri)
bom_response = execute(catFactory, updated_order_request)

pprint(bom_response)
# pprint(jsonify(bom_response))