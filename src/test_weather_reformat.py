import json
import boto3
from moto import mock_sqs
import weather_reformat as wf

AWS_REGION = 'us-east-1'
QUEUE_NAME = "willow"

def test_to_f():
    assert wf.to_f(77) == 170.6
    assert wf.to_f(-12) == 10.4
    assert wf.to_f(0) == 32.0
    

def test_format():
    target = json.loads(w1)
    wf.format(target)
    assert 'lat' in target['coord'] and target['coord']['lat'] == 32.06329
    assert 'lon' in target['coord'] and target['coord']['lon'] == 12.52859
    assert 'unique_insert_key' in target
    assert 'timestamp' in target
    assert target['timestamp'].index('T') > 0
    assert 1485784982000 == target['dt']

@mock_sqs
def test_format_and_send(monkeypatch):

    monkeypatch.setenv("QUEUE_NAME", QUEUE_NAME)
    monkeypatch.setenv('AWS_REGION', AWS_REGION)

    boto3.setup_default_session(region_name = AWS_REGION)
    client = boto3.client("sqs")
    resource = boto3.resource("sqs")

    client.create_queue(QueueName=QUEUE_NAME)

    data = dict()
    data['cod'] = 200
    data['cnt'] = 1
    data['list'] = [json.loads(w1)]

    assert wf.format_and_send(json.dumps(data))['statusCode'] == 200

    queue  = resource.get_queue_by_name(QueueName=QUEUE_NAME)
    message_out = client.receive_message(QueueUrl = queue.url)
    body = message_out['Messages'][0]['Body'] 
    assert json.loads(body)['id'] == 2208791


w1 = """
{  
   "id":2208791,
   "name":"Yafran",
   "coord":{  
      "Lon":12.52859,
      "Lat":32.06329
   },
   "main":{  
      "temp":9.68,
      "temp_min":9.681,
      "temp_max":9.681,
      "pressure":961.02,
      "sea_level":1036.82,
      "grnd_level":961.02,
      "humidity":85
   },
   "dt":1485784982,
   "wind":{  
      "speed":3.96,
      "deg":356.5
   },
   "rain":{  
      "3h":0.255
   },
   "clouds":{  
      "all":88
   },
   "weather":[  
      {  
         "id":500,
         "main":"Rain",
         "description":"light rain",
         "icon":"10d"
      }
   ]
}
"""