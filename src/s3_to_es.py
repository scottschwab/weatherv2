import json
import logging
import os
import sys

import boto3
sys.path.append("./3rdparty")
from requests_aws4auth import AWS4Auth
import requests

logging.basicConfig(level = logging.INFO)

logger = logging.getLogger(__name__)

# ENV variables used
# AWS_REGION - set by AWS
# ES_HOST
# ES_INDEX
# ES_INDEX_TYPE
# S3_BUCKET
# S3_OBJECT_PREFIX
# S3_OBJECT_POSTFIX
# REMOVE_OLD


HEADERS = { 'Content-Type' : 'application/json'}

CREDENTIALS = boto3.Session().get_credentials()
AWSAUTH = AWS4Auth(CREDENTIALS.access_key, CREDENTIALS.secret_key, 
    os.getenv('AWS_REGION'), "es", session_token=CREDENTIALS.token)

INDEX_PATH = f"{os.getenv('ES_INDEX')}/{os.getenv('ES_INDEX_TYPE')}"

PREFIX = os.environ.get('S3_OBJECT_PREFIX')
POSTFIX = os.environ.get('S3_OBJECT_POSTFIX')
BUCKET = os.environ.get('S3_BUCKET')

def push_record(record):
    url = f"https://{os.getenv('ES_HOST')}/{INDEX_PATH}"
    response = requests.post(url, auth=AWSAUTH, json=json.loads(record), 
        headers=HEADERS)
    print(response)

def move_files():
    client = boto3.client('s3')
    resource = boto3.resource('s3')
    objects = client.list_objects(Bucket=BUCKET)
    print(len(objects))
    print(list(objects.keys()))
    key_name = objects['Contents'][2]['Key']
    print(key_name)
    if key_name[0:3] == PREFIX and key_name[-5:] == POSTFIX:
        print(key_name)
        logger.info(f"processing {key_name}")
        obj = resource.Object(BUCKET, key_name)
        content = obj.get()['Body'].read()
        push_record(content)

def transfer_files(event, context):
    move_files()
