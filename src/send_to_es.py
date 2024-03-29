"""
Given a json document from a SQS queue, it is placed
on an AWS ES server. 
"""
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
    """Given a json document, based on environmental variables,
       the document is pushed to the ES endpoint.  If the 
       'unique_insert_key' is defined, it is used as the
       document id, to insure that only one copy of the 
       document is placed in ES.
    """ 
    try:
        logging.debug(body)
        body_json = json.loads(body)
        url = f"https://{os.getenv('ES_HOST')}/{INDEX_PATH}"
        if 'unique_insert_key' in body_json:
            url = f"{url}/{body_json['unique_insert_key']}/_create"
            print(url)
            response = requests.put(url, auth=AWSAUTH, json=body_json, 
                headers=HEADERS)
        else:
            response = requests.post(url, auth=AWSAUTH, json=body_json, 
                headers=HEADERS)
                
        print(response)
    except Exception as err:
        print(err)
        m = f"Unable to store data due to {err}"
        logger.error(m)
        return {
            'statusCode': 500,
            'body': m
        }    

def send_to_es(event, context):
    """This is the lambda entry point, which sends the
       document to be put in ES and removes the message
       from the queue.
    """

    resource = boto3.resource('sqs')
    client = boto3.client('sqs')
    print("number of records " + str(len(event['Records'])))
    for rec in event['Records']:
        send_body_to_es(rec['body'])
    
        # Going by documentation, removing the message from 
        # the queue should not be required, but from testing
        # it is needed.
        qn = rec['eventSourceARN'].split(':')[-1]
        queue = resource.get_queue_by_name(QueueName=qn)
        client.delete_message(
            QueueUrl=queue.url,
            ReceiptHandle=rec['receiptHandle']
        )
    return 
