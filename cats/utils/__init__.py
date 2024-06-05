import os, time, json, subprocess
from copy import deepcopy
from pprint import pprint


class Dict2Class(object):
    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


def subproc_run(cmd):
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True
    )


def catSubmit(order_request, meshClient):
    print("Order:")
    order = json.loads(meshClient.cat(order_request["order_cid"]))
    print()
    pprint(order)
    print()

    ppost = lambda args, endpoint: \
        f'curl -X POST -H "Content-Type: application/json" -d \\\n\'{json.dumps(**args)}\' {endpoint}'
    post = lambda args, endpoint: \
        'curl -X POST -H "Content-Type: application/json" -d \'' + json.dumps(**args) + f'\' {endpoint}'

    post_cmd = post({'obj': order_request}, order["endpoint"])
    print(ppost({'obj': order_request}, order["endpoint"]))
    print()
    print()
    response_str = subprocess.check_output(post_cmd, shell=True)
    output_bom = json.loads(response_str)

    output_bom['POST'] = post_cmd
    return output_bom


def flatten_bom(bom_response, meshClient):
    invoice = json.loads(
        meshClient.cat(bom_response["bom"]["invoice_cid"])
    )
    invoice['order'] = json.loads(
        meshClient.cat(invoice['order_cid']),
    )
    invoice['order']['flat'] = {
        'function': json.loads(meshClient.cat(invoice['order']["function_cid"])),
        'invoice': json.loads(meshClient.cat(invoice['order']["invoice_cid"]))
    }
    bom_response["flat_bom"] = {
        'invoice': invoice,
        'log': json.loads(
            meshClient.cat(bom_response["bom"]["log_cid"])
        )
    }
    return bom_response


def create_order_request(
    ingress_obj,
    process_obj,
    egress_obj,
    data_dirpath,
    structure_filepath,
    meshClient,
    JOB_HOME,
    endpoint='http://127.0.0.1:5000/cat/node/execute'
):
    structure_cid, structure_name = meshClient.cidFile(structure_filepath)
    function = {
        'ingress_subproc_cid': meshClient.ipfsClient.add_pyobj(ingress_obj),
        'integration_subproc_cid': meshClient.ipfsClient.add_pyobj(process_obj),
        'egress_subproc_cid': meshClient.ipfsClient.add_pyobj(egress_obj),
        'infrafunction_cid': None
    }
    invoice = {
        "data_cid": meshClient.cidDir(data_dirpath)
    }
    order = {
        "function_cid": meshClient.ipfsClient.add_str(json.dumps(function)),
        "structure_cid": structure_cid,
        "invoice_cid": meshClient.ipfsClient.add_str(json.dumps(invoice)),
        "structure_filepath": structure_name,
        "JOB_HOME": JOB_HOME,
        "endpoint": endpoint
    }
    order_request = {
        'order_cid': meshClient.ipfsClient.add_str(json.dumps(order))
    }
    return order_request


def linkProcess(
        cat_response,
        meshClient,
        ingress_subproc=None,
        integration_subproc=None,
        egress_subproc=None
):
    flattened_bom = flatten_bom(cat_response, meshClient)
    flat_bom = deepcopy(flattened_bom['flat_bom'])
    function_cids = flat_bom['invoice']['order']['flat']['function']
    function = {'infrafunction_cid': None}
    if ingress_subproc is not None:
        function['ingress_subproc_cid'] = meshClient.ipfsClient.add_pyobj(ingress_subproc)
    else:
        function['ingress_subproc_cid'] = function_cids['ingress_subproc_cid']
    if integration_subproc is not None:
        function['integration_subproc_cid'] = meshClient.ipfsClient.add_pyobj(integration_subproc)
    else:
        function['integration_subproc_cid'] = function_cids['integration_subproc_cid']
    if egress_subproc is not None:
        function['egress_subproc_cid'] = meshClient.ipfsClient.add_pyobj(egress_subproc)
    else:
        function['egress_subproc_cid'] = function_cids['egress_subproc_cid']
    new_function_cid = meshClient.ipfsClient.add_str(json.dumps(function))

    invoice = flat_bom['invoice']
    input_invoice = {'data_cid': invoice['data_cid']}
    new_invoice_cid = meshClient.ipfsClient.add_str(json.dumps(input_invoice))

    order = invoice['order']
    order['function_cid'] = new_function_cid
    order['invoice_cid'] = new_invoice_cid
    del order['flat']
    order['endpoint'] = 'http://127.0.0.1:5000/cat/node/link'

    order_request = {'order_cid': meshClient.ipfsClient.add_str(json.dumps(order))}
    return order_request


def wait_for_directory(directory_path, check_interval=1):
    """
    Waits until the specified directory exists.

    :param directory_path: The path to the directory to wait for.
    :param check_interval: Time (in seconds) between checks.
    """
    while not os.path.exists(directory_path):
        print(f"Waiting for directory: {directory_path}")
        time.sleep(check_interval)
    print(f"Directory {directory_path} now exists.")


def read_exit_code(file_path):
    try:
        with open(file_path, 'r') as file:
            exit_code_str = file.read().strip()
            exit_code = int(exit_code_str)
            return exit_code
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
    except ValueError:
        print(f"Error: The file {file_path} does not contain a valid exit code.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def wait_for_directory_to_be_populated(directory_path, check_interval=1, timeout=None):
    """
    Waits until the specified directory contains at least one file.

    :param directory_path: The path to the directory to monitor.
    :param check_interval: Time (in seconds) between checks. Default is 1 second.
    :param timeout: Maximum time (in seconds) to wait. None for no timeout. Default is None.
    :return: True if the directory was populated, False if timed out.
    """
    start_time = time.time()

    while True:
        # Check if the directory contains any files
        if os.path.isdir(directory_path) and os.listdir(directory_path):
            print(f"Directory '{directory_path}' is populated.")
            return True

        # Check if timeout has been reached
        if timeout and (time.time() - start_time) > timeout:
            print(f"Timeout reached. Directory '{directory_path}' is still empty.")
            return False

        # Wait for the specified interval before checking again
        time.sleep(check_interval)


def flatten_bom(bom_response, meshClient):
    invoice = json.loads(
        meshClient.cat(bom_response["bom"]["invoice_cid"])
    )
    invoice['order'] = json.loads(
        meshClient.cat(invoice['order_cid']),
    )
    invoice['order']['flat'] = {
        'function': json.loads(meshClient.cat(invoice['order']["function_cid"])),
        'invoice': json.loads(meshClient.cat(invoice['order']["invoice_cid"]))
    }
    bom_response["flat_bom"] = {
        'invoice': invoice,
        'log': json.loads(
            meshClient.cat(bom_response["bom"]["log_cid"])
        )
    }
    return bom_response