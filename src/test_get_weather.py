"""
 These are unit test for the get_weather calls, but since
 mocking the sqs and http request do not play nice, not
 testing the methods that need both.

"""
import boto3
import pytest
import sys
from moto import mock_sqs

import get_weather as gw

AWS_REGION = 'us-east-1'
REQUEST_PATH = "/data/2.5/box/city"
NORTH = 40
SOUTH = 20
EAST = -90
WEST = -100
SCALE = 100
API_KEY = "dog"

BB = f"bbox={WEST},{NORTH},{EAST},{SOUTH},{SCALE}"
PATH = f"{REQUEST_PATH}?{BB}&APPID={API_KEY}"

QUEUE_NAME = "cat"



def test_getbbox():
    assert gw.get_bbox(NORTH, WEST, SOUTH, EAST, SCALE) == BB

def test_get_appid(monkeypatch):
    monkeypatch.setenv('API_KEY', API_KEY) 
    assert gw.get_appid() == f"APPID={API_KEY}"

def test_get_path(monkeypatch): 
    monkeypatch.setenv('API_KEY', API_KEY)
    monkeypatch.setenv('REQUEST_PATH', REQUEST_PATH)
    assert gw.get_path(NORTH, WEST, SOUTH, EAST, SCALE) == PATH

@mock_sqs
def test_add_to_queue(monkeypatch):
    monkeypatch.setenv("QUEUE_NAME", QUEUE_NAME)
    monkeypatch.setenv('AWS_REGION', AWS_REGION)

    boto3.setup_default_session(region_name = AWS_REGION)
    client = boto3.client("sqs")
    resource = boto3.resource("sqs")

    client.create_queue(QueueName=QUEUE_NAME)

    message_in = b'mouse'
    gw.add_to_queue(message_in)

    queue  = resource.get_queue_by_name(QueueName=QUEUE_NAME)
    message_out = client.receive_message(QueueUrl = queue.url) 
    assert message_out['Messages'][0]['Body'] == str(message_in, encoding='utf-8')
