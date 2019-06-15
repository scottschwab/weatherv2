# weatherv2
aws lambda weather


# Overview
This is a simple workflow set to pull data from openweathermap.com and store it into an elasticsearch system, hosted in AWS.  The moving of data is done by lamda funtions, by the way of AWS SMS and S3.

## Design

### Current
The current implementation is:
```
                                   Cloud Watch Event (run every 30 min)
                                                |
                                             kick off
                                                 |
                                                 V
<www.openweathermap.com>  -- pull --> [lambda: get_weather] --------> SMS -------------+
                                                                                       |
       +-------------------------------------------------------------------------------+
       |
       +--->[lambda: reformatWeather] --> S3 Bucket --> [lambda: s3_elasticsearch] --> ES
```

### Next
Upon reflection, the next version will be somthing like
```
                                   Cloud Watch Event (run every 30 min)
                                                |
                                             kick off
                                                 |
                                                 V
<www.openweathermap.com>  -- pull --> [lambda: get_weather] --------> S3 Bucket -------+
                                                                                       |
       +-------------------------------------------------------------------------------+
       |
       +--->[lambda: joined of reformatWeather and lambda: s3_elasticsearch] --> ES
```
The advantage being that any records pulled from openweathermap.com could be put 
unaltered in the s3 storage bucket, and the read from s3 will reformat and store
the data, instead of requiring previous to s3 prep work.





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
* To remove all data from an index: `curl -XDELETE https://search-elastic-1-43l4n5p5ht73jjobi7ba6te634.us-east-1.es.amazonaws.com/weather `

* In install a schema: `curl --header "Content-type: application/json" -XPUT https://search-elastic-1-43l4n5p5ht73jjobi7ba6te634.us-east-1.es.amazonaws.com/weather_v2 -d@weather_schema.json`

* To query directory `curl --header "Content-type: application/json" -XGET https://search-elastic-1-43l4n5p5ht73jjobi7ba6te634.us-east-1.es.amazonaws.com/weather_v2/_search -d"{\"query\": { \"match\": { \"name\": \"Crystal City\" }}}" `, see https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html for details.

## TODO:
1. Improve unit testing, including the mocking of http request and sms queue.
2. Bulk upload of historical data to show searching of larger datasets.
