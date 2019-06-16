import json
import datetime as dt
import logging
import os
import sys

import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_to_sqs(body):
    client = boto3.client("sqs")
    queues = client.list_queues(QueueNamePrefix = os.environ.get("QUEUE_NAME"))
    queue_url = queues['QueueUrls'][0]
    response = client.send_message(
        MessageBody = json.dumps(body),
        QueueUrl = queue_url,
        DelaySeconds = 0
    )
    #print(response)

def to_f(c):
    return round(c * 9 / 5.0 + 32, 1)

def format(city):
    t = dt.datetime.fromtimestamp(city['dt'], dt.timezone.utc)
    city['timestamp'] = t.isoformat(sep='T')
    city['dt'] = int(city['dt']) * 1000
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
    resource = boto3.resource('sqs')
    client = boto3.client('sqs')

    for rec in event['Records']:
        format_and_send(rec['body'])

        # should not be needed, goin by the docs, but removing processed message
        qn = rec['eventSourceARN'].split(':')[-1]
        queue = resource.get_queue_by_name(QueueName=qn)
        client.delete_message(
            QueueUrl=queue.url,
            ReceiptHandle=rec['receiptHandle']
        )
    return
