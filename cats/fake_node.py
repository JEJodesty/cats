import json
from pprint import pprint
from cats import SERVICE

order_request = {'order_cid': 'QmNU5EAmWNDc7U3bjZ8X2rzjD3iN83KXcarsvnyk8AXA9o'}
order_request["order"] = json.loads(SERVICE.meshClient.cat(order_request["order_cid"]))
order_request['invoice'] = json.loads(SERVICE.meshClient.cat(order_request['order']['invoice_cid']))

ipfs_uri = f'ipfs://{order_request["invoice"]["data_cid"]}/*.csv'
catFactory, updated_order_request = SERVICE.initFactory(order_request, ipfs_uri)
bom_response = SERVICE.execute(catFactory, updated_order_request)

pprint(bom_response)
# pprint(jsonify(bom_response))