import os
import ipfsapi as ipfsApi
from os.path import dirname, abspath

from cats.network import MeshClient
from cats.service import Service

CWD = os.getcwd()
CATS_HOME = dirname(dirname(abspath(__file__)))
MESH_CLIENT = MeshClient(
    ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
)
SERVICE = Service(
    meshClient=MESH_CLIENT,
    CATS_HOME=CATS_HOME
)
DATA_HOME = SERVICE.DATA_HOME
JOB_HOME = SERVICE.JOB_HOME
CACHE_HOME = SERVICE.CACHE_HOME
INPUT_PLANT_HOME = SERVICE.INPUT_PLANT_HOME
INPUT_DATA_HOME = SERVICE.INPUT_DATA_HOME
print(CATS_HOME)
print(DATA_HOME)
print(JOB_HOME)
print(CACHE_HOME)
