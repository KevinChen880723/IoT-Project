from __future__ import print_function
import json
import boto3
  
print('Loading function')
  
def lambda_handler(event, context):
  
    # Parse the JSON message 
    eventText = "IoT Device's power is turned "+json.dumps(event["power"])
    eventText = eventText+"and LED color is changed to "
    eventText = eventText+json.dumps(event["color"])
  
    # Print the parsed JSON message to the console; you can view this text in the Monitoring tab in the Lambda console or in the CloudWatch Logs console
    print('Received event: ', eventText)
  
    # Create an SNS client
    sns = boto3.client('sns')
    # Publish a message to the specified topic
    response = sns.publish (
      TopicArn = 'arn:aws:sns:us-east-1:643656783849:kevinSNSTopic1225',
      Message = eventText
    )
    print(response)
