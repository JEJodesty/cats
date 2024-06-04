import os
import ipfsapi as ipfsApi
from os.path import dirname, abspath
import boto3 as boto3
from cats.network import MeshClient
from cats.service import Service

CWD = os.getcwd()
CATS_HOME = dirname(dirname(abspath(__file__)))
SERVICE = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    ),
    CATS_HOME=CATS_HOME
)
DATA_HOME = SERVICE.DATA_HOME
JOB_HOME = SERVICE.JOB_HOME
CACHE_HOME = SERVICE.CACHE_HOME
print(CATS_HOME)
print(DATA_HOME)
print(JOB_HOME)
print(CACHE_HOME)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_CLIENT = boto3.client(
    's3',
    region_name='us-east-2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
