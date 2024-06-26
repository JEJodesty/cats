import subprocess
from typing import Dict
import numpy as np
import ray

from cats.utils import executeCMD


def docker_ipfs_cmd(input_dir_cid, output_dir, container):
    return (
        f"docker exec {container} sh -c '"
        f"ipfs get {input_dir_cid} -o {output_dir} && "
        f"cd {output_dir} && "
        f"rm -f api config datastore_spec gateway repo.lock version && "
        f"ipfs add -r ."
        f"'"
    )


run_ipfs_container = lambda x: f"""
if [ ! "$(docker ps -q -f name=ipfs-{x})" ]; then
  # Check if the container exists but is not running
  if [ "$(docker ps -aq -f status=exited -f name=ipfs-{x})" ]; then
      # Cleanup
      docker rm ipfs-{x}
  fi
  # Run the container
  docker run -d --name ipfs-{x} ipfs/go-ipfs
else
  echo "ipfs-{x} is already running."
fi
"""


def ipfs_migration(input_dir_cid, migration, output_dir='/outputs/data'):
    executeCMD(run_ipfs_container(migration))
    cmd = docker_ipfs_cmd(input_dir_cid, output_dir, container='ipfs-migration')
    print(cmd)
    try:
        # Execute the Docker command
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )

        # Check if the command was successful
        if result.returncode == 0:
            # Parse the output to get the CID
            output_lines = result.stdout.splitlines()
            for line in output_lines:
                if line.startswith('added') and line.endswith('data'):
                    # The CID is the second element in the space-separated line
                    cid = line.split()[1]
                    return cid
            return "CID not found in the output."
        else:
            return f"Command failed with error: {result.stderr}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

def ingress(input_dir_cid):
    return ipfs_migration(input_dir_cid=input_dir_cid, migration='ingress')

def egress(input_dir_cid):
    return ipfs_migration(input_dir_cid=input_dir_cid, migration='egress')

run_integration_container = lambda v_output_dir, output_dir: f"""
if [ ! "$(docker ps -q -f name=ipfs-integration)" ]; then
  # Check if the container exists but is not running
  if [ "$(docker ps -aq -f status=exited -f name=ipfs-integration)" ]; then
      # Cleanup
      docker rm ipfs-integration
  fi
  # Run the container
  docker run -d --name ipfs-integration -v {v_output_dir}:{output_dir} ipfs/go-ipfs
else
  echo "ipfs-integration is already running."
fi
"""


def integration_cache(input_dir_cid: str, v_output_dir, output_dir='/outputs'):
    print("Integration Cache:")
    executeCMD(run_integration_container(v_output_dir, output_dir))
    cmd = docker_ipfs_cmd(input_dir_cid, output_dir, container='ipfs-integration')
    try:
        # Execute the Docker command
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )

        # Check if the command was successful
        if result.returncode == 0:
            # Parse the output to get the CID
            output_lines = result.stdout.splitlines()
            for line in output_lines:
                if line.startswith('added') and line.endswith('data'):
                    # The CID is the second element in the space-separated line
                    cid = line.split()[1]
                    return cid
            return "CID not found in the output."
        else:
            return f"Command failed with error: {result.stderr}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


def function_0(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    vec_a = batch["petal length (cm)"]
    vec_b = batch["petal width (cm)"]
    batch["petal area (cm^2)"] = vec_a * vec_b
    return batch


def function_1(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    vec_a = batch["petal length (cm)"]
    vec_b = batch["petal width (cm)"]
    batch["DUPLICATE petal area (cm^2)"] = vec_a * vec_b
    return batch


def process_0(input, output):
    ray.init()
    ds_in = ray.data.read_csv(input)
    ds_out = ds_in.map_batches(function_0)
    idx_ds = ray.data.range(ds_out.count())
    ds_out = idx_ds.zip(ds_out)
    print(ds_out.show(limit=1))
    ds_out.write_csv(output)
    ray.shutdown()
    return ds_out


def process_1(input, output):
    ray.init()
    ds_in = ray.data.read_csv(input)
    ds_out = ds_in.map_batches(function_1)
    print(ds_out.show(limit=1))
    ds_out.write_csv(output)
    ray.shutdown()
    return ds_out
