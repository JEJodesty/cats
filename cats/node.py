from cats import SERVICE
import logging, json, traceback
from flask import Flask, request, jsonify

catNode = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set level to DEBUG for more detailed logging
logger = logging.getLogger(__name__)


@catNode.route('/cat/node/init', methods=['POST'])
def execute_init_cat():
    try:
        order_request = request.get_json()
        order_request["order"] = json.loads(SERVICE.meshClient.cat(order_request["order_cid"]))
        order_request['invoice'] = json.loads(SERVICE.meshClient.cat(order_request['order']['invoice_cid']))

        # IPFS checks
        # if 'bom_cid' not in bom:
        #     return jsonify({'error': 'CID not provided'}), 400

        ipfs_uri = f'ipfs://{order_request["invoice"]["data_cid"]}/*.csv'
        catFactory, updated_order_request = SERVICE.initFactory(order_request, ipfs_uri)
        bom_response = SERVICE.execute(catFactory, updated_order_request)

        # Return BOM
        response = jsonify(bom_response)
        return response

    except Exception as e:
        logger.error("An error occurred: %s", traceback.format_exc())
        response = jsonify({'error': str(e)})
        return response


@catNode.route('/cat/node/link', methods=['POST'])
def execute_link_cat():
    try:
        order_request = request.get_json()
        order_request["order"] = json.loads(SERVICE.meshClient.cat(order_request["order_cid"]))
        order_request['invoice'] = json.loads(SERVICE.meshClient.cat(order_request['order']['invoice_cid']))

        prev_data_cid = order_request['invoice']['data_cid']
        data_cid = SERVICE.meshClient.linkData(prev_data_cid)
        ipfs_uri = f'ipfs://{data_cid}/*.csv'
        catFactory, updated_order_request = SERVICE.initFactory(order_request, ipfs_uri)
        bom_response = SERVICE.execute(catFactory, updated_order_request)

        # Return BOM
        return jsonify(bom_response)

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    # Run the Flask application on http://127.0.0.1:5000/
    catNode.run(debug=True)