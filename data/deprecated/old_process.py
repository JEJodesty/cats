import subprocess
from pprint import pprint
from typing import Dict
import numpy as np
import ray

# def docker_ipfs_cmd(container, input_dir_cid, output_dir):
#     return (
#         f"docker exec {container} sh -c '"
#         f"ipfs get {input_dir_cid} -o {output_dir} && "
#         f"cd {output_dir} && "
#         f"rm -f api config datastore_spec gateway repo.lock version && "
#         f"ipfs add -r ."
#         f"'"
#     )

def docker_compose_yaml(container_name, input_cid, output_dir, container_cmd):
    return f"""
    services:
      ipfs_worker:
        image: ipfs/go-ipfs:latest
        container_name: {container_name}  # Replace this with your IPFS container image
        command: >
          {container_cmd(input_cid, output_dir)}
    """

def docker_compose_yaml(container_name, service_name, output_dir='/outputs/data'):
    file_str = f"""
services:
  {service_name}:
    image: ipfs/go-ipfs:latest
    container_name: {container_name}  # Replace this with your IPFS container image
    """
    file_path = f"./structure/{container_name}_compose.yaml"
    with open(file_path, "w") as file:
        file.write(file_str)

    compose_cmd = f"""
docker-compose -f {file_path} exec {service_name} sh -c \n \
'ipfs get QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN -o {output_dir} && \n \
rm -f api config datastore_spec gateway repo.lock version && \n \
chmod -R 777 .'
    """
    """
    docker-compose -f data/input/structure/ipfs_transport_compose.yaml exec ipfs_migration_worker sh -c '
        ipfs get QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN -o /outputs/data &&
        rm -f api config datastore_spec gateway repo.lock version &&
        chmod -R 777 .
    '
    """

    return compose_cmd

def migration_cmd(input_cid, output_dir):
    return f"sh -c 'ipfs get {input_cid} -o {output_dir} && cd {output_dir} && rm -f api config datastore_spec gateway repo.lock version && ipfs add -r .'"

odir = "/Users/joshua/Projects/cats/data/deprecated"
print(docker_compose_yaml(container_name="ipfs_migration", service_name="ipfs_worker", output_dir='/outputs/data'))
# docker-compose -f data/input/structure/ipfs_migration_compose.yaml exec ipfs_worker sh -c 'ipfs get QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN -o outputs && rm -f api config datastore_spec gateway repo.lock version && chmod -R 777 .'
exit()

def ipfs_migration(input_dir_cid, container_name='ipfs-migration', output_dir='/outputs/data'):
    try:
        # Execute the Docker command
        result = subprocess.run(
            """
            docker-compose -f data/input/structure/ipfs_transport_compose.yaml exec ipfs_migration_worker sh -c '
                ipfs get QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN -o /outputs/data &&
                rm -f api config datastore_spec gateway repo.lock version &&
                chmod -R 777 .
            '
            """,
            input=docker_compose_yaml(container_name=container_name, input_cid=input_dir_cid, output_dir=output_dir, container_cmd=migration_cmd),
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
            pprint(output_lines)
            return "CID not found in the output."
        else:
            return f"Command failed with error: {result.stderr}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

def ingress(input_dir_cid):
    return ipfs_migration(input_dir_cid=input_dir_cid)

def egress(input_dir_cid):
    return ipfs_migration(input_dir_cid=input_dir_cid)

def integration_cmd(input_cid, output_dir):
    return f"sh -c 'ipfs get {input_cid} -o {output_dir} && rm -f api config datastore_spec gateway repo.lock version && chmod -R 777 .'"

def integration_cache(input_dir_cid: str, cwd: str): #, v_output_dir, output_dir='/output'):
    print("Integration Cache:")

    # exec_cmd = docker_ipfs_cmd(container="ipfs-integration", input_cid=input_dir_cid, output_dir='outputs', cmd=integration_cmd)
    # f"""
    # docker exec ipfs-integration \
    # sh -c 'ipfs get {input_dir_cid} -o outputs && rm -f api config datastore_spec gateway repo.lock version && chmod -R 777 .'
    # """
    # print(exec_cmd)
    try:
        # Execute the Docker command
        result = subprocess.run(
            'docker-compose -f - up --scale ipfs_worker=1',
            input=docker_compose_yaml(container_name="ipfs-integration", input_cid=input_dir_cid, output_dir='outputs', container_cmd=integration_cmd),
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
            pprint(output_lines)
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
