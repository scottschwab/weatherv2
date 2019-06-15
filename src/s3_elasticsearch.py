import json
import logging
import os
import sys

import boto3

# AWS does not include the AWS4Auth or requests library
# by default, so it must be loaded with the lambda
sys.path.append("./3rdparty")
from requests_aws4auth import AWS4Auth
import requests

logging.basicConfig(level = logging.WARNING)

logger = logging.getLogger(__name__)

# ENV variables used
# AWS_REGION - set by AWS
# ES_HOST
# ES_INDEX
# ES_INDEX_TYPE
# S3_BUCKET
# S3_OBJECT_PREFIX
# S3_OBJECT_POSTFIX


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

def cleanup(resource, key_name):
    bucket = resource.Bucket(BUCKET)
    bucket.delete_objects(
        Delete={"Objects":[{"Key":key_name}],"Quiet":True})
    
def move_files():
    client = boto3.client('s3')
    resource = boto3.resource('s3')
    objects = client.list_objects(Bucket=BUCKET)
    key_name = objects['Contents'][2]['Key']
    print(key_name)
    if key_name[0:len(PREFIX)] == PREFIX and key_name[-len(POSTFIX):] == POSTFIX:
            
        logger.info(f"processing {key_name}")
        obj = resource.Object(BUCKET, key_name)
        content = obj.get()['Body'].read()
        push_record(content)
        cleanup(resource, key_name)


def transfer_files(event, context):
    move_files()
