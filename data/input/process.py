import multiprocessing, os, subprocess, time, ray
from typing import Dict

import numpy as np

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


def _run_ray_batches(input, output, batch_fn, zip_with_range):
    """Ray Data work for a single CAT process invocation.

    Runs inside an isolated subprocess started by `_ray_run`, so its Ray
    session - and any objects/refs it creates - is fully torn down when
    the subprocess exits.
    """
    ray.init(ignore_reinit_error=True)
    try:
        ds_in = ray.data.read_csv(input)
        print(ds_in.schema())
        print()
        ds_out = ds_in.map_batches(batch_fn)
        if zip_with_range:
            ds_out = ds_out.materialize()
            ds_out = ray.data.range(ds_out.count()).zip(ds_out)
        print(ds_out.show(limit=1))
        ds_out.write_csv(output)
        return output
    finally:
        ray.shutdown()


def _ray_subprocess_entry(target, args, result_queue):
    """Top-level, picklable entry point for the subprocess spawned by
    `_ray_run` (required since `multiprocessing`'s "spawn" context can
    only launch picklable, module-level callables)."""
    try:
        result_queue.put(('ok', target(*args)))
    except BaseException as exc:
        try:
            result_queue.put(('error', exc))
        except Exception:
            # exc may not itself be picklable; fall back to a plain
            # message so the parent still observes the failure.
            result_queue.put(('error', RuntimeError(f'{type(exc).__name__}: {exc}')))


def _ray_run(target, *args):
    """Run `target(*args)` in a fresh subprocess with its own isolated
    Ray session.

    Repeatedly calling `ray.shutdown()`/`ray.init()` within the same
    long-lived process (the CAT node) doesn't fully release Ray's
    internal session state, which eventually surfaces as "trying to
    access Ray objects whose owner is unknown" errors on later CAT
    process invocations. Running each invocation in its own subprocess
    avoids this entirely, since process exit forces complete teardown.
    """
    ctx = multiprocessing.get_context('spawn')
    result_queue = ctx.Queue()
    proc = ctx.Process(target=_ray_subprocess_entry, args=(target, args, result_queue))
    proc.start()
    proc.join()

    if result_queue.empty():
        raise RuntimeError(
            f'Ray worker subprocess exited unexpectedly '
            f'(exit code {proc.exitcode}) without returning a result.'
        )
    status, payload = result_queue.get()
    if status == 'error':
        raise payload
    return payload


def process_0(input, output):
    return _ray_run(_run_ray_batches, input, output, function_0, True)


def process_1(input, output):
    return _ray_run(_run_ray_batches, input, output, function_1, False)
