# weatherv2
aws lambda weather


# Overview
This is a simple workflow set to pull data from openweathermap.com and store it into an elasticsearch system, hosted in AWS.  The moving of data is done by lamda funtions, by the way of AWS SQS message queues.

## Design

### Current
The current implementation is:
```
                                Cloud Watch Event (run every 30 min)
                                                |
                                             kick off
                                                |
                                                V
<www.openweathermap.com>  -- pull --> [lambda: get_weather]
                                                |
                                     <sqs: weather_to_format>
                                                |
                                                V
                                    [lambda: weather_reformat]
                                                |
                                  <sqs: weather_to_format_to_es>
                                                |
                                                V
                                    [lambda: send_to_es] -- put/post --> ES
```


# Access

## Account on AWS
* Link: https://console.aws.amazon.com/iam/
* Account ID or Alias: `codebyscott`
* IAM user name: `demo.elastic`

## View collected weather data
* Kibana: https://search-elastic-1-43l4n5p5ht73jjobi7ba6te634.us-east-1.es.amazonaws.com/_plugin/kibana/
* ElasticSearch: https://search-elastic-1-43l4n5p5ht73jjobi7ba6te634.us-east-1.es.amazonaws.com/

## Deployment
1. cd into the src directory.
2. zip up the files and 3rdparty subidrectory into a zip file on that level (next to .py files).
3. Upload that zip into AWS lambda.
4. Map functions to proper lambda methods.
5. Test.

## Elasticsearch Details
* To remove all data from an index: `curl -XDELETE https://search-elastic-1-43l4n5p5ht73jjobi7ba6te634.us-east-1.es.amazonaws.com/weather_v5`

* In install a schema: `curl --header "Content-type: application/json" -XPUT https://search-elastic-1-43l4n5p5ht73jjobi7ba6te634.us-east-1.es.amazonaws.com/weather_v5 -d@weather_schema.json `

* To query directory ` curl --header "Content-type: application/json" -XGET https://search-elastic-1-43l4n5p5ht73jjobi7ba6te634.us-east-1.es.amazonaws.com/weather_v5/_search -d"{\"query\": { \"match\": { \"name\": \"Jacksonville\" }}}"`, see https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html for details.

## TODO:
1. Add testing for send_to_es.py.
2. Figure out how to test with both http mock and s3 mode
3. Bulk upload of historical data to show searching of larger datasets.

