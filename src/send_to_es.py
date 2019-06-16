import json
import logging
import os
import sys

import boto3

# AWS does not include the AWS4Auth or requests library
# by default, so it must be loaded with the lambda
sys.path.append("./3rdparty")
import requests
from requests_aws4auth import AWS4Auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CREDENTIALS = boto3.Session().get_credentials()
AWSAUTH = AWS4Auth(CREDENTIALS.access_key, CREDENTIALS.secret_key, 
    os.getenv('AWS_REGION'), "es", session_token=CREDENTIALS.token)


# ENV variables used
# AWS_REGION - set by AWS
# ES_HOST
# ES_INDEX
# ES_INDEX_TYPE

HEADERS = { 'Content-Type' : 'application/json'}
INDEX_PATH = f"{os.getenv('ES_INDEX')}/{os.getenv('ES_INDEX_TYPE')}"

def send_body_to_es(body):
    try:
        logging.debug(body)
        url = f"https://{os.getenv('ES_HOST')}/{INDEX_PATH}"
        response = requests.post(url, auth=AWSAUTH, json=json.loads(body), 
            headers=HEADERS)
        print(response)
    except Exception as err:
        m = f"Unable to store data due to {err}"
        logger.error(m)
        return {
            'statusCode': 500,
            'body': m
        }    

def send_to_es(event, context):
    for rec in event['Records']:
        send_body_to_es(rec['body'])
