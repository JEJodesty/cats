import os
import sys

# Ray's `uv run` integration rebuilds an isolated per-worker virtualenv from
# pyproject.toml's base `dependencies` only, which omits `ray` itself (it
# lives under the optional `ops` extra) - workers then fail with
# `ModuleNotFoundError: No module named 'ray'`. Disabling it makes workers
# inherit this process's own environment instead, where `ray` is already
# installed. Must be set before anything below can spawn a Ray worker.
os.environ.setdefault('RAY_ENABLE_UV_RUN_RUNTIME_ENV', '0')

# Running this file by path (`python cats/node.py`) only puts its own
# directory - not the repo root - on sys.path. `data/` (holding
# data/input/process.py's ingress/egress/integration functions) lives at
# the repo root, sibling to `cats/`, and isn't part of the installed `cats`
# package - so it's only importable once the repo root is on sys.path.
# That's needed here because InfraFunction unpickles those functions by
# their `data.input.process` module path (see
# cats/executor/function/__init__.py), which requires `import data` to
# succeed in *this* process.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import logging, json, traceback

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