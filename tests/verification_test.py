### Execute Initial CAT0:
##### Instantiate CAT Mesh Client:

from pprint import pprint
import pandas as pd

from cats import MESH_CLIENT as meshClient
from cats import INPUT_STRUCTURE_HOME, INPUT_DATA_HOME

##### Compose Initial CAT Order request for CAT Node

from data.input.process import *
cat_order_request_0 = meshClient.create_order_request(
    ingress_subproc=ingress,
    integrated_subproc=process_0,
    egress_subproc=egress,
    integration_cache_subproc=integration_cache,
    data_dirpath=INPUT_DATA_HOME, # f'{INPUT_DATA_HOME}/iris.csv',
    structure_filepath=f'{INPUT_STRUCTURE_HOME}/main.tf',
    endpoint='http://127.0.0.1:5000/cat/node/init'
)
pprint(cat_order_request_0)

##### Submit Initial CAT Order request to CAT Node

cat_invoiced_response_0 = meshClient.catSubmit(cat_order_request_0)
pprint(cat_invoiced_response_0)
flat_cat_invoiced_response_0 = meshClient.flatten_bom(cat_invoiced_response_0)
pprint(flat_cat_invoiced_response_0)

### Execute CAT1:
##### Compose a modified CAT Order request that executes CAT1 with CAT0's Structure a new Process

cat_order_request_1 = meshClient.create_order_request(
    ingress_subproc=ingress,
    integrated_subproc=process_1,
    egress_subproc=egress,
    integration_cache_subproc=integration_cache,
    data_dirpath=INPUT_DATA_HOME, # f'{INPUT_DATA_HOME}/iris.csv',
    structure_filepath=f'{INPUT_STRUCTURE_HOME}/main.tf',
    endpoint='http://127.0.0.1:5000/cat/node/init'
)
pprint(cat_order_request_0)

##### Submit modified CAT Order request to CAT Node

cat_invoiced_response_1 = meshClient.catSubmit(cat_order_request_1)
pprint(cat_invoiced_response_1)
flat_cat_invoiced_response_1 = meshClient.flatten_bom(cat_invoiced_response_1)
pprint(flat_cat_invoiced_response_1)