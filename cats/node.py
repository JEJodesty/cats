import logging, json, traceback
from pprint import pprint

from flask import Flask, request, jsonify
from cats import SERVICE

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

        catFactory, updated_order_request = SERVICE.initFactory(
            order_request, order_request["invoice"]["data_cid"]
        )
        bom_response = SERVICE.execute(catFactory, updated_order_request)

        # Return BOM
        response = jsonify(bom_response)
        return response

    except Exception as e:
        logger.error("An error occurred: %s", traceback.format_exc())
        response = jsonify({'error': str(e)})
        return response


if __name__ == '__main__':
    # Run the Flask application on http://127.0.0.1:5000/
    catNode.run(debug=True)