import os
import subprocess
import time
from typing import Dict

import numpy as np
import ray

from cats.network.ipfs_docker import (
    IPFS_GET_TIMEOUT,
    MIGRATION_CONTAINER,
    INTEGRATION_CONTAINER,
    ensure_docker_ipfs_peers,
)

STRUCTURE_HOME = os.path.join(os.path.dirname(__file__), 'structure')


def docker_ipfs_cmd(container, input_dir_cid, output_dir):
    return (
        f"docker exec {container} sh -c '"
        f'ipfs get {input_dir_cid} -o {output_dir} && '
        f'cd {output_dir} && '
        f"rm -f api config datastore_spec gateway repo.lock version && "
        f"ipfs add -r ."
        f"'"
    )


def _run_docker_ipfs(cmd, cwd=None):
    ensure_docker_ipfs_peers()
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd or STRUCTURE_HOME,
        timeout=IPFS_GET_TIMEOUT,
    )


def ipfs_migration(input_dir_cid, container=MIGRATION_CONTAINER):
    unix_ts = int(time.time())
    output_dir = f'/outputs/data_{unix_ts}'
    cmd = docker_ipfs_cmd(container, input_dir_cid, output_dir)
    try:
        result = _run_docker_ipfs(cmd)

        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            for line in output_lines:
                print(line)
                if line.startswith('added') and line.endswith(f'data_{unix_ts}'):
                    cid = line.split()[1]
                    return cid, f'data_{unix_ts}'
            return "CID not found in the output."
        return f"Command failed with error: {result.stderr}"

    except subprocess.TimeoutExpired:
        return (
            f"Command timed out after {IPFS_GET_TIMEOUT}s fetching CID {input_dir_cid}. "
            "Ensure `ipfs daemon` is running on the host and Docker IPFS nodes are peered."
        )
    except Exception as e:
        return f"An error occurred: {str(e)}"


def ingress(input_dir_cid):
    return ipfs_migration(input_dir_cid=input_dir_cid)


def egress(input_dir_cid):
    result = ipfs_migration(input_dir_cid=input_dir_cid)
    if isinstance(result, tuple):
        return result[0]
    return result


def integration_cache(
    input_dir_cid: str,
    cwd: str,
    container=INTEGRATION_CONTAINER,
):
    print("Integration Cache:")
    exec_cmd = (
        f"docker exec {container} "
        f"sh -c 'ipfs get {input_dir_cid} -o outputs && "
        f"rm -f api config datastore_spec gateway repo.lock version && chmod -R 777 .'"
    )
    print(exec_cmd)
    try:
        result = _run_docker_ipfs(exec_cmd, cwd=cwd)

        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            for line in output_lines:
                if line.startswith('added') and line.endswith('data'):
                    cid = line.split()[1]
                    return cid
            return "CID not found in the output."
        return f"Command failed with error: {result.stderr}"

    except subprocess.TimeoutExpired:
        return (
            f"Command timed out after {IPFS_GET_TIMEOUT}s fetching CID {input_dir_cid}. "
            "Ensure `ipfs daemon` is running on the host and Docker IPFS nodes are peered."
        )
    except Exception as e:
        return f"An error occurred: {str(e)}"


def function_0(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    vec_a = batch["petal length (cm)"].astype('double')
    vec_b = batch["petal width (cm)"].astype('double')
    batch["petal area (cm^2)"] = vec_a * vec_b
    return batch


def function_1(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    vec_a = batch["petal length (cm)"].astype('double')
    vec_b = batch["petal width (cm)"].astype('double')
    batch["DUPLICATE petal area (cm^2)"] = vec_a * vec_b
    return batch


def _ray_run(work):
    """Start a clean local Ray session for each CAT process invocation."""
    if ray.is_initialized():
        ray.shutdown()
    ray.init(ignore_reinit_error=True)
    try:
        return work()
    finally:
        ray.shutdown()


def process_0(input, output):
    def work():
        ds_in = ray.data.read_csv(input)
        print(ds_in.schema())
        print()
        ds_out = ds_in.map_batches(function_0).materialize()
        ds_out = ray.data.range(ds_out.count()).zip(ds_out)
        print(ds_out.show(limit=1))
        ds_out.write_csv(output)
        return output

    return _ray_run(work)


def process_1(input, output):
    def work():
        ds_in = ray.data.read_csv(input)
        print(ds_in.schema())
        print()
        ds_out = ds_in.map_batches(function_1)
        print(ds_out.show(limit=1))
        ds_out.write_csv(output)
        return output

    return _ray_run(work)
