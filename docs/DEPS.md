##### Platform Dependencies:
0. [**Docker:**](https://docs.docker.com/desktop/install/mac-install/)
1. [**uv**](https://docs.astral.sh/uv/) (>= 0.7.0) — manages the pinned Python interpreter, virtual environment
  (`.venv`), and locked dependencies (`uv.lock`) for CATs. Install it, then let it install the Python version
  pinned in [`.python-version`](../.python-version):
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  cd <path-to>/cats
  uv python install   # installs Python 3.12.5 per .python-version; no separate Python install needed
  ```
  (See [`ENV.md`](./ENV.md) for the full `uv sync` / `uv run` workflow.)
2. [**kind**](https://kind.sigs.k8s.io/docs/user/quick-start/#installing-from-release-binaries) (>= 0.20.0)
3. [**kubectl**](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/) (>= 1.27.3")
4. [**helm**](https://helm.sh/docs/intro/install/) (>= 3.12.1)
5. [**Terraform**:](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) (>= 1.15.7)
  * Use Terraform's standalone binary if `brew install` fails due to an outdated Xcode, download the official precompiled binary directly and place it on your `PATH` (e.g. the project's `.venv/bin`, created by `uv sync`):
```bash
cd <path-to>/cats
VER=1.15.7   # adjust as needed
curl -LO "https://releases.hashicorp.com/terraform/${VER}/terraform_${VER}_darwin_arm64.zip"
unzip "terraform_${VER}_darwin_arm64.zip"
mv terraform .venv/bin/
rm "terraform_${VER}_darwin_arm64.zip"
terraform -version
# > Note: use `darwin_amd64` instead of `darwin_arm64` on Intel Macs. After installing, restart
#  > `cats/node.py` so the running process picks up the new binary on `PATH`.
#  > When running Terraform manually from the repo root:
#  >   export TF_DATA_DIR="$PWD/data/input/structure/.terraform-data"
#  >   export INTEGRATION_INPUT_DATA_CACHE="$PWD/data/cache/integration/outputs"
#  > (Use absolute paths; docker-compose treats relative volume paths as named volumes.)
```
6. [**Go**](https://go.dev/dl/) (>= v3.13.1)
7. [**IPFS Kubo**](https://docs.ipfs.tech/install/command-line/#system-requirements) (>= 0.21.0)
  (See [`IPFS.md`](./IPFS.md) for running/managing the host daemon.)