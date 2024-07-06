import subprocess
from typing import Dict
import numpy as np
import ray


def docker_ipfs_cmd(container, input_dir_cid, output_dir):
    return (
        f"docker exec {container} sh -c '"
        f"ipfs get {input_dir_cid} -o {output_dir} && "
        f"cd {output_dir} && "
        f"rm -f api config datastore_spec gateway repo.lock version && "
        f"ipfs add -r ."
        f"'"
    )

# run_ipfs_container = lambda container: f"""
# # Check if the container is running
# if [ "$(docker ps -q -f name={container})" ]; then
#     echo "Stopping the running container: {container}"
#     docker stop {container}
# fi
#
# # Check if the container exists (but is not running)
# if [ "$(docker ps -aq -f name={container})" ]; then
#     echo "Removing the existing container: {container}"
#     docker rm {container}
# fi
#
# echo "Starting a new container: {container}"
# docker run -d --name {container} ipfs/go-ipfs
# """
#
# start_ipfs_daemon = lambda container: f"docker exec {container} ipfs daemon &"


# """
# # Check if the new container is running
# if [ "$(docker ps -q -f name={container})" ]; then
#     echo "The container {container} is up and running."
# else
#     echo "Failed to start the container {container}."
# fi
# """


def ipfs_migration(input_dir_cid, container='ipfs-migration', output_dir='/outputs/data'):
    cmd = docker_ipfs_cmd(container, input_dir_cid, output_dir)
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
    return ipfs_migration(input_dir_cid=input_dir_cid)

def egress(input_dir_cid):
    return ipfs_migration(input_dir_cid=input_dir_cid)

# run_integration_container = lambda v_output_dir: f"""
# if [ ! "$(docker ps -q -f name=ipfs-integration)" ]; then
#   # Check if the container exists but is not running
#   if [ "$(docker ps -aq -f status=exited -f name=ipfs-integration)" ]; then
#       # Cleanup
#       docker stop ipfs-integration
#       docker rm ipfs-integration
#   fi
#   # Run the container
#   docker run -d --name ipfs-integration -v {v_output_dir}:/output ipfs/go-ipfs
#   input_dir_cid, output_dir, container
# else
#   echo "ipfs-integration is already running."
# fi
# """


def integration_cache(input_dir_cid: str, cwd: str): #, v_output_dir, output_dir='/output'):
    print("Integration Cache:")
    exec_cmd = f"""
    docker exec ipfs-integration \
    sh -c 'ipfs get {input_dir_cid} -o outputs && rm -f api config datastore_spec gateway repo.lock version && chmod -R 777 .'
    """
    print(exec_cmd)
    try:
        # Execute the Docker command
        result = subprocess.run(
            exec_cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd
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
    vec_a = batch["petal length (cm)"].astype('double')
    vec_b = batch["petal width (cm)"].astype('double')
    batch["petal area (cm^2)"] = vec_a * vec_b
    return batch


def function_1(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    vec_a = batch["petal length (cm)"].astype('double')
    vec_b = batch["petal width (cm)"].astype('double')
    batch["DUPLICATE petal area (cm^2)"] = vec_a * vec_b
    return batch


def process_0(input, output):
    ray.init()
    ds_in = ray.data.read_csv(input)
    print(ds_in.schema())
    print()
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
    print(ds_in.schema())
    print()
    ds_out = ds_in.map_batches(function_1)
    print(ds_out.show(limit=1))
    ds_out.write_csv(output)
    ray.shutdown()
    return ds_out
