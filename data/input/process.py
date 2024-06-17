from typing import Dict
import numpy as np
import ray

from cats.utils.cod import codSubmit


def ingress(input_dir: str):
    print("Ingress:")
    cmd = f"""
    bacalhau docker run --id-only --wait -p ipfs -i {input_dir} alpine:3.20.0 -- sh -c 'cp -r /inputs/* /'
    """
    print(cmd)
    return codSubmit(cmd)


def integration_cache(input_dir: str, output_dir: str = None, download: str = False):
    print("Integration Cache:")
    if download is True:
        download = "--download"
    else:
        download = ""
    cmd = f"""
    bacalhau docker run --id-only --wait {download} -i {input_dir} --output-dir {output_dir} \
    alpine:3.20.0 -- sh -c 'cp -r /inputs/* /'
    """
    print(cmd)
    return codSubmit(cmd)


def egress(input_dir: str):
    print("Egress:")
    cmd = f"""
    bacalhau docker run --id-only --wait -p ipfs -i {input_dir} alpine:3.20.0 -- sh -c 'cp -r /inputs/* /outputs/'
    """
    print(cmd)
    return codSubmit(cmd)


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
