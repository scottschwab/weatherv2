"""
This lambda retrieves a document with multiple weather entries
from a SQS queue, breaks it into individual weather entries,
reformats some data in the entry, and finally pushes each
individual weather entries onto a different SQS message queue.
"""
import json
import datetime as dt
import logging
import os
import sys

import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_to_sqs(body):
    """Takes a json document, as a string, and places it on a SQS queue."""
    client = boto3.client("sqs")    
    resource = boto3.resource("sqs")
    queue = resource.get_queue_by_name(QueueName=os.getenv("QUEUE_NAME"))
    response = client.send_message(
        MessageBody = json.dumps(body),
        QueueUrl = queue.url,
        DelaySeconds = 0
    )
    #print(response)

def to_f(c):
    """Convert Celsius to Fahrenheit"""
    return round(c * 9 / 5.0 + 32, 1)

def format(city):
    """Takes in a weather entry and formats into a ES friendly version.
       - The coordinate of the point is put into a ES geo_point entry.
       - The timestamp is converted from seconds to milliseconds.
       - The temperatures are converted into Fahrenheit.
       - A unique key is created, to prevent duplicate date in ES.
    """
    t = dt.datetime.fromtimestamp(city['dt'], dt.timezone.utc)
    city['timestamp'] = t.isoformat(sep='T')
    city['dt'] = int(city['dt']) * 1000
    if 'Lat' in city['coord']:
        lat = city['coord']['Lat']
        lon = city['coord']['Lon']
        city['coord'].pop('Lat')
        city['coord'].pop('Lon')
        city['coord']['lat'] = lat
        city['coord']['lon'] = lon
    city['main']['temp'] = to_f(city['main']['temp'])
    city['main']['temp_min'] = to_f(city['main']['temp_min'])
    city['main']['temp_max'] = to_f(city['main']['temp_max'])
    city['unique_insert_key'] = city['dt'] + city['id']
    return city

def format_and_send(body):
    """This routine is given a document with multiple weather
       entries and is breaks it appart based on the city tags.
       Each city entry is reformated and sent off to a SQS queue.
    """
    data = json.loads(body)
    if (data['cod'] != 200):
        m = f"Unable to store data due to request error {data['cod']}"
        logging.error(m)
        return {
            'statusCode': 500,
            'body': m
        }
    try:
        for city in data['list']:
            city_out = format(city)
            send_to_sqs(city_out)
        return {
            'statusCode': 200,
            'body': f"Stored {data['cnt']} weather events"
        }
    except Exception as err:
        m = f"Unable to store data at due to {err}"
        logger.error(m)
        return {
            'statusCode': 500,
            'body': m
        }

def translate(event, context):
    """This is the lambda entry routine, which is given 
       a document of weather entries, sends if off to be
       broken up, formatted, and forwarded along.
    """
    resource = boto3.resource('sqs')
    client = boto3.client('sqs')

    for rec in event['Records']:
        format_and_send(rec['body'])

        # should not be needed, going by the docs, 
        # but for now we emoving processed message
        qn = rec['eventSourceARN'].split(':')[-1]
        queue = resource.get_queue_by_name(QueueName=qn)
        client.delete_message(
            QueueUrl=queue.url,
            ReceiptHandle=rec['receiptHandle']
        )
    return
