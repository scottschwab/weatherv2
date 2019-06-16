import http
import os
import boto3

HOST="api.openweathermap.org"
REQUEST_PATH="/data/2.5/box/city"

def get_bbox(north, west, south, east, scale):
    if north < south:
        raise ValueError(f"north {north} below south {south}")
    if east < west:
        raise ValueError(f"east {east} is west {west} of west")
    if scale < 1:
        raise ValueError(f"scale {scale} must be positive")
    return f"bbox={west},{north},{east},{south},{scale}"

def get_appid():
    key = os.environ.get("API_KEY")
    return f"APPID={key}"

def get_path(north, west, south, east, scale):
    return f"{REQUEST_PATH}?{get_bbox(north, west, south, east, scale)}&{get_appid()}"

def pull(north, west, south, east, scale = 100):
    client = http.client.HTTPConnection(HOST)

    request = client.request("GET",get_path(north, west, south, east, scale))
    response = client.getresponse()
    add_to_queue(response.read())

def add_to_queue(message):
    client = boto3.client("sqs")
    queues = client.list_queues(QueueNamePrefix = os.environ.get("QUEUE_NAME"))
    queue_url = queues['QueueUrls'][0]
    response = client.send_message(
        MessageBody = str(message, 'utf-8'),
        QueueUrl = queue_url,
        DelaySeconds = 0
    )


def env_pull(event, message):
    north = float(os.environ.get("NORTH"))
    south = float(os.environ.get("SOUTH"))
    east = float(os.environ.get("EAST"))
    west = float(os.environ.get("WEST"))
    scale = int(os.environ.get("SCALE"))
    pull(north, west, south, east, scale)
