import json
import boto3
import datetime as dt
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

bucket = "elasticsearch.demo.codebyscott.com"
postfix = "json"



s3 = boto3.resource('s3')    
now =  str(dt.datetime.utcnow())

def store_to_s3(body_text):
    """
    Take a json documented, as returned by the openweather api and store
    it into the s3 bucket, under an name derved by city code and date time.

    Also stick a user friendly date and time into the document
    """
    logging.debug(body_text)
    data = json.loads(body_text)

    logging.info(list(data.keys()))
    if (data['cod'] != 200):
        m = f"Unable to store data at {now} due to request error {data['cod']}"
        logging.error(m)
        return {
            'statusCode': 500,
            'body': m
        }
    try:
        # TODO: handle "null" for rain and snow
        print(f"cities found {len(data['list'])}")
        for city in data['list']:
            t = dt.datetime.fromtimestamp(city['dt'], dt.timezone.utc)
            city['timestamp'] = t.isoformat(sep='T')
            city['dt'] = int(city['dt']) * 1000
            lat = city['coord']['Lat']
            lon = city['coord']['Lon']
            city['coord'].pop('Lat')
            city['coord'].pop('Lon')
            city['coord']['lat'] = lat
            city['coord']['lon'] = lon
            
            name = f"in_{city['id']}_{t}.{postfix}"
            name = name.replace(' ', '_')
            s3.Object(bucket, name).put(
                Body=json.dumps(city, indent=2).encode('utf-8')
            )    
        return {
            'statusCode': 200,
            'body': f"Stored {data['cnt']} weather events at {now}"
        }
    except Exception as err:
        m = f"Unable to store data at {now} due to {err}"
        logger.error(m)
        return {
            'statusCode': 500,
            'body': m
        }
        
def translate(event, context):
    for rec in event['Records']:
        store_to_s3(rec['body'])