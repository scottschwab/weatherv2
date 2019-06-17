"""
This is the front end of the weatger to ES processing queue.  
It is kicked off by a Cloud Watch Event and this lambda makes 
a request to the http://api.openweathermap.org endpoint for 
all the data points in a bounding box.  The bounds are defined
by environmental variables.

The result of the query is single json document that contains 
multiple entries, one for each location.  This document is 
pushed onto a SQS queue, and that triggers the next step
in the workflow.

"""

import http
import os
import boto3

HOST="api.openweathermap.org"
REQUEST_PATH="/data/2.5/box/city"

def get_bbox(north, west, south, east, scale):
    """Generate a bounding box url arguement."""
    if north < south:
        raise ValueError(f"north {north} below south {south}")
    if east < west:
        raise ValueError(f"east {east} is west {west} of west")
    if scale < 1:
        raise ValueError(f"scale {scale} must be positive")
    return f"bbox={west},{north},{east},{south},{scale}"

def get_appid():
    """Set the API_KEY from the environment."""
    key = os.environ.get("API_KEY")
    return f"APPID={key}"

def get_path(north, west, south, east, scale):
    """Combine elements to build the query path."""
    return f"{REQUEST_PATH}?{get_bbox(north, west, south, east, scale)}&{get_appid()}"

def add_to_queue(message):
    """Place the message onto the SQS queue."""
    client = boto3.client("sqs")    
    resource = boto3.resource("sqs")
    queue  = resource.get_queue_by_name(QueueName=os.getenv("QUEUE_NAME"))
    response = client.send_message(
        MessageBody = str(message, 'utf-8'),
        QueueUrl = queue.url,
        DelaySeconds = 0
    )

def pull(north, west, south, east, scale = 100):
    """Build and pull the data from the endpoint."""
    client = http.client.HTTPConnection(HOST)

    request = client.request("GET",get_path(north, west, south, east, scale))
    response = client.getresponse()
    add_to_queue(response.read())

def env_pull(event, message):
    """Based on the environmental variables, pull the data and put 
       it on the queue.
    """
    north = float(os.environ["NORTH"])
    south = float(os.environ["SOUTH"])
    east = float(os.environ["EAST"])
    west = float(os.environ["WEST"])
    scale = int(os.environ["SCALE"])
    pull(north, west, south, east, scale)
