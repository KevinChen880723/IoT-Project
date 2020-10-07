import json
import boto3
import ast

def lambda_handler(event, context):
    # TODO implement
    #body = eval(event['body'].replace("'", ""))
    
    shadow = boto3.client('iot-data')
    httpMethod = event["httpMethod"]
    # Set the default update data
    updateData = {
        "state" : {
            "desired" : {
                "color" : "blue",
                "power" : "off"
            }
        }
    }
    # The IoT Thing We Want To Control, this is set as required parameter
    thing = event["pathParameters"]["shadowname"]
    
    if httpMethod == "PUT":
        try:
            body = ast.literal_eval(event['body'])
            
            if "color" in body:
                updateData["state"]["desired"]["color"] = body["color"]
            if "power" in  body:
                updateData["state"]["desired"]["power"] = body["power"]
            
            
            returnValue = shadow.update_thing_shadow(
                thingName = thing,
                payload = json.dumps(updateData)
            )
            #returnValue = json.loads(returnValue['payload'].read())["state"]
            returnValue = "success!"
            returnstatus = 200
        except:
            returnstatus = 404
            returnValue = "false!"
        
    elif httpMethod == "GET":
        try:
            print("GET")
            returnValue = shadow.get_thing_shadow(
                thingName = thing
            )
            returnValue = json.loads(returnValue['payload'].read())
            print(returnValue)
            returnstatus = 200
        except:
            returnValue = "Shadow doesn't exist"
            returnstatus = 404
            
    elif httpMethod == "DELETE":
        try:
            returnValue = shadow.delete_thing_shadow(
                thingName = thing
            )
            print("delete")
            returnValue = json.loads(returnValue['payload'].read())
            returnstatus = 200
        except:
            returnValue = "Shadow doesn't exist"
            returnstatus = 404
            
    return {
        'statusCode': returnstatus,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE,PUT"
        },
        'body': json.dumps(returnValue)
    }
