import os
import re

from cats.utils import subproc_run

KIND_CLUSTER_NAME = "cats"
KIND_CLUSTER_RESOURCE = "kind_cluster.default"
APPLIED_STRUCTURE_MARKER = '.applied-structure.cid'


def _applied_structure_marker_path(structure_home):
    return os.path.join(structure_home, APPLIED_STRUCTURE_MARKER)


def read_applied_structure_cid(structure_home):
    """Return the structure_cid this Structure's Terraform state currently
    reflects, or None if nothing has been successfully applied yet."""
    marker_path = _applied_structure_marker_path(structure_home)
    if not os.path.isfile(marker_path):
        return None
    with open(marker_path, encoding='utf-8') as marker_file:
        return marker_file.read().strip() or None


def write_applied_structure_cid(structure_home, structure_cid):
    """Record the structure_cid Terraform state now reflects, so a later
    CAT execution with an unchanged (content-addressed) Structure can
    reconcile in place instead of destroying and rebuilding the Plant."""
    with open(_applied_structure_marker_path(structure_home), 'w', encoding='utf-8') as marker_file:
        marker_file.write(structure_cid or '')


def terraform_bin(service):
    # `.venv` is uv's managed venv (see docs/DEPS.md).
    path = os.path.join(service.CATS_HOME, '.venv', 'bin', 'terraform')
    return path if os.path.isfile(path) else 'terraform'


def configure_terraform_data_dir(structure_home):
    # TF_DATA_DIR must not equal the module root; that breaks backend state loading.
    tf_data_dir = os.path.join(structure_home, '.terraform-data')
    os.makedirs(tf_data_dir, exist_ok=True)
    os.environ['TF_DATA_DIR'] = tf_data_dir
    return tf_data_dir


def ensure_integration_cache_env(service):
    # Docker Compose bind mounts require an absolute host path; relative paths
    # are treated as named volumes and fail with "undefined volume".
    cache = os.path.abspath(service.INTEGRATION_INPUT_DATA_CACHE)
    os.makedirs(cache, exist_ok=True)
    os.environ['INTEGRATION_INPUT_DATA_CACHE'] = cache
    return cache


def _parse_lock_providers(lock_path):
    providers = []
    current = None
    with open(lock_path, encoding='utf-8') as lock_file:
        for line in lock_file:
            provider_match = re.match(
                r'\s*provider\s+"registry\.terraform\.io/([^"]+)"',
                line,
            )
            if provider_match:
                current = provider_match.group(1)
                continue
            if current:
                version_match = re.match(r'\s*version\s*=\s*"([^"]+)"', line)
                if version_match:
                    providers.append((current, version_match.group(1)))
                    current = None
    return providers


def _provider_binary_present(platform_path):
    for name in os.listdir(platform_path):
        path = os.path.join(platform_path, name)
        if os.path.isfile(path) and os.access(path, os.X_OK) and 'terraform-provider' in name:
            return True
    return False


def providers_cached(structure_home):
    lock_path = os.path.join(structure_home, '.terraform.lock.hcl')
    tf_data_dir = os.path.join(structure_home, '.terraform-data')
    if not os.path.isfile(lock_path) or not os.path.isdir(tf_data_dir):
        return False

    required = _parse_lock_providers(lock_path)
    if not required:
        return False

    for provider, version in required:
        version_dir = os.path.join(
            tf_data_dir,
            'providers',
            'registry.terraform.io',
            provider,
            version,
        )
        if not os.path.isdir(version_dir):
            return False
        if not any(
            _provider_binary_present(os.path.join(version_dir, platform))
            for platform in os.listdir(version_dir)
            if os.path.isdir(os.path.join(version_dir, platform))
        ):
            return False
    return True


def _terraform_state_resources(service, structure_home):
    configure_terraform_data_dir(structure_home)
    proc = subproc_run(
        f'{terraform_bin(service)} state list',
        cwd=structure_home,
    )
    if proc.returncode != 0:
        return set()
    return {line.strip() for line in proc.stdout.splitlines() if line.strip()}


def _kind_cluster_names():
    proc = subproc_run('kind get clusters')
    if proc.returncode != 0:
        return set()
    return {line.strip() for line in proc.stdout.splitlines() if line.strip()}


def cleanup_orphan_kind_cluster(service, structure_home):
    """Remove a leftover kind cluster when it exists on the host but not in state."""
    clusters = _kind_cluster_names()
    if KIND_CLUSTER_NAME not in clusters:
        return

    state = _terraform_state_resources(service, structure_home)
    if KIND_CLUSTER_RESOURCE in state:
        return

    print(
        f'Removing orphan kind cluster "{KIND_CLUSTER_NAME}" '
        f'({KIND_CLUSTER_RESOURCE} is not in Terraform state)'
    )
    proc = subproc_run(f'kind delete cluster --name {KIND_CLUSTER_NAME}')
    if proc.returncode != 0:
        raise RuntimeError(
            f'Failed to delete orphan kind cluster "{KIND_CLUSTER_NAME}": {proc.stderr.strip()}'
        )
    if proc.stdout.strip():
        print(proc.stdout.strip())


class Plant:
    def __init__(self, service):
        self.service = service
        self.INPUT_STRUCTURE_HOME = self.service.INPUT_STRUCTURE_HOME
        tf_data_dir = configure_terraform_data_dir(self.INPUT_STRUCTURE_HOME)
        cache_dir = ensure_integration_cache_env(self.service)
        print(f"export TF_DATA_DIR={tf_data_dir}")
        print(f"export INTEGRATION_INPUT_DATA_CACHE={cache_dir}")


class InfraStructure:
    def __init__(self, service):
        self.service = service
        self.INPUT_STRUCTURE_HOME = self.service.INPUT_STRUCTURE_HOME
        configure_terraform_data_dir(self.INPUT_STRUCTURE_HOME)
        ensure_integration_cache_env(self.service)
        print(
            f"Environment variable INTEGRATION_INPUT_DATA_CACHE is set to:",
            os.environ["INTEGRATION_INPUT_DATA_CACHE"]
        )

    def destroy(self):
        print('Destroy Structure!')
        self.service.executeCMD(
            f'{terraform_bin(self.service)} destroy --auto-approve',
            cwd=self.INPUT_STRUCTURE_HOME
        )
        print()
        print()

    def plan(self):
        print('Plan Structure!')
        self.service.executeCMD(
            f'{terraform_bin(self.service)} plan',
            cwd=self.INPUT_STRUCTURE_HOME
        )
        print()
        print()

    def initialize(self):
        print('Initialize Structure!')
        configure_terraform_data_dir(self.INPUT_STRUCTURE_HOME)
        if providers_cached(self.INPUT_STRUCTURE_HOME):
            print('Terraform providers already cached; skipping init.')
            print()
            return
        self.service.executeCMD(
            f'{terraform_bin(self.service)} init -input=false',
            cwd=self.INPUT_STRUCTURE_HOME
        )
        print()
        print()

    def apply(self):
        print('Apply Structure!')
        configure_terraform_data_dir(self.INPUT_STRUCTURE_HOME)
        ensure_integration_cache_env(self.service)
        cleanup_orphan_kind_cluster(self.service, self.INPUT_STRUCTURE_HOME)
        self.service.executeCMD(
            f'{terraform_bin(self.service)} apply --auto-approve',
            cwd=self.INPUT_STRUCTURE_HOME
        )
        peer_script = os.path.join(self.INPUT_STRUCTURE_HOME, 'ipfs_connect_peers.sh')
        if os.path.isfile(peer_script):
            print('Connect IPFS transport peers...')
            proc = subproc_run(f'bash {peer_script}', cwd=self.INPUT_STRUCTURE_HOME)
            if proc.stdout.strip():
                print(proc.stdout.strip())
            if proc.returncode != 0 and proc.stderr.strip():
                print(proc.stderr.strip())
        print()
        print()