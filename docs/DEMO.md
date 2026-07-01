## [Establish a CAT Mesh:](../cats_demo.py)
#### Steps:
##### 0. Start Docker daemon *in Terminal A*:
##### 1. Start IPFS daemon *in Terminal B*:
```bash
ipfs daemon
```
* **Optional:** 
  * Shut down IPFS daemon: `ipfs shutdown`
##### 2. [Create Virtual Environment](./docs/ENV.md)
```bash
# CATs working directory
cd cats
python -m venv ./venv
```
##### 3. Activate Virtual Environment and install dependencies *in Terminal C*:
```bash
source ./venv/bin/activate
# (venv) $
pip install -e ".[ops]"
```
`[ops]` adds Marimo, Ray, and pandas for the mesh workflow; pytest is included in the base install.
##### 4. Deploy CAT Node *in Terminal D*:
```bash
# (venv) $
PYTHONPATH=./ python cats/node.py
```
##### 5. Establish Data (CAT) Mesh *in Terminal C*: [Demo](../cats_demo.py)
Execute a CATs on a single node Mesh via Marimo Notebook.
```bash
# (venv) $
marimo edit cats_demo.py
```
Cells re-run reactively as dependencies change; work through the notebook top to bottom.
