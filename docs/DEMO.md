## [Establish a CAT Mesh:](../cats_demo.ipynb)
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
##### 3. Activate Virtual Environment *in Terminal C*:
```bash
source ./venv/bin/activate
# (venv) $
```
##### 4. Deploy CAT Node *in Terminal D*:
```bash
# (venv) $
PYTHONPATH=./ python cats/node.py
```
##### 5. Establish Data (CAT) Mesh *in Terminal C*: [Demo](../cats_demo.ipynb) 
Execute a CATs on a single node Mesh.
```bash
# (venv) $
jupyter notebook cats_demo.ipynb
# Run > Run All Cells
```