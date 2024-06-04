import json
from pprint import pprint

from cats.factory import Factory
from cats import SERVICE


def initFactory(order_request, ipfs_uri, service=SERVICE):
    service.initBOMcar(
        structure_cid=order_request['order']['structure_cid'],
        structure_filepath=order_request['order']['structure_filepath'],
        function_cid=order_request['order']['function_cid'],
        init_data_cid=ipfs_uri
    )
    catFactory = Factory(service)
    return catFactory, order_request


def execute(catFactory, order_request, service=SERVICE):
    executor = catFactory.produce()
    enhanced_bom, _ = executor.execute()

    invoice = {}
    enhanced_bom['invoice']['order_cid'] = service.ipfsClient.add_str(
        json.dumps(order_request['order'])
    )
    invoice['invoice_cid'] = service.ipfsClient.add_str(
        json.dumps(enhanced_bom['invoice'])
    )
    invoice['invoice'] = enhanced_bom['invoice']

    bom = {
        'log_cid': enhanced_bom['log_cid'],
        'invoice_cid': invoice['invoice_cid']
    }
    bom_response = {
        'bom': bom,
        'bom_cid': service.ipfsClient.add_str(json.dumps(bom))
    }
    return bom_response


order_request = {'order_cid': 'QmNU5EAmWNDc7U3bjZ8X2rzjD3iN83KXcarsvnyk8AXA9o'}
order_request["order"] = json.loads(SERVICE.meshClient.cat(order_request["order_cid"]))
order_request['invoice'] = json.loads(SERVICE.meshClient.cat(order_request['order']['invoice_cid']))

ipfs_uri = f'ipfs://{order_request["invoice"]["data_cid"]}/*.csv'
catFactory, updated_order_request = initFactory(order_request, ipfs_uri)
bom_response = execute(catFactory, updated_order_request)

pprint(bom_response)
# pprint(jsonify(bom_response))