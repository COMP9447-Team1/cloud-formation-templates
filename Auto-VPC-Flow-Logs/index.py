import json
import boto3
import time
import os
import random
import urllib3 
http = urllib3.PoolManager() # not sure not why inside of def - is it executed only once?


def lambda_handler(event, context):
    # NOTE: This main function was SLIGHTLY updated
    # Change: added 'result' var so the same strings can be re-used
    # PS. Still not as good as the proper OOP programming with different classes etc, but that's something right?
    result = "Event handling failed for unknown reasons" #default string
    
    # Grab non-logged VPC ID from Security Hub finding
    print(event)
    print(context)
    
    invokingEvent = json.loads(event["invokingEvent"])
    noncompliantVPC = invokingEvent["configurationItem"]["configuration"]["vpcId"]
    VPCName = invokingEvent["configurationItem"]["configuration"]["tags"][0]["value"]
    
    # import lambda runtime vars
    lambdaFunctionName = os.environ['AWS_LAMBDA_FUNCTION_NAME']
    # Get Flow Logs Role ARN from function config
    client = boto3.client('lambda')
    role_response = (client.get_function_configuration(
        FunctionName = os.environ['AWS_LAMBDA_FUNCTION_NAME'])
    )
    print(role_response)
    deliverLogsPermissionArn = role_response['Role']
    # Import boto3 clients
    cwl = boto3.client('logs')
    ec2 = boto3.client('ec2')
    # set dynamic variable for CW Log Group for VPC Flow Logs
    print('ncvpc: ', noncompliantVPC)
    vpcFlowLogGroup = "VPCFlowLogs/" + noncompliantVPC
    # create cloudwatch log group
    print("trying to create log group")
    try:
        create_log_grp = cwl.create_log_group(logGroupName=vpcFlowLogGroup)
    except Exception as e:
        print(e)
        print("failed creating log group")
        raise              
    # wait for CWL creation to propagate
    # create VPC Flow Logging
    
    print("trying to create enable flow logs")
    try:
        enableFlowlogs = ec2.create_flow_logs(
        DryRun=False,
        DeliverLogsPermissionArn=deliverLogsPermissionArn,
        LogGroupName=vpcFlowLogGroup,
        ResourceIds=[ noncompliantVPC ],
        ResourceType='VPC',
        TrafficType='REJECT',
        LogDestinationType='cloud-watch-logs'
        )
        print(enableFlowlogs)
    except Exception as e:
        print("trying to create enable flow logs failed")

        print(e)
        raise
    # wait for Flow Log creation to propogate
    # searches for flow log status, filtered on unique CW Log Group created earlier
    print('trying to describe flowlogs')
    try:
        confirmFlowlogs = ec2.describe_flow_logs(
        DryRun=False,
        Filters=[
            {
                'Name': 'log-group-name',
                'Values': [ vpcFlowLogGroup ]
            },
        ]
        )
        flowStatus = str(confirmFlowlogs['FlowLogs'][0]['FlowLogStatus'])
        if flowStatus == 'ACTIVE':
            result = 'Flow logging is now SUCCESSFULLY enabled for VPC ' + noncompliantVPC + ' with name ' + VPCName
        else:
            result = "Enabling VPC flow logging failed! Remediate manually"
            print(result)
            return 1
    except Exception as e:
        print(e)
        print('trying to describe flowlogs failed')
        raise

    # === Slack Notifications part ====
    print('trying to send to slack')

    try: #  try logic to catch errors
        # parameters
        channel = "{{INSERT_CHANNEL_NAME_HERE}}"
        url = "{{INSERT_SLACK_WEBHOOK_HERE}}"
                
        # my own var
        md_text = "*"+( event.get('detail-type', "Config Rule") + "*\n\n" +
            result + "\n\n"
            #event.get('description', "-description is not currently present for this event-")  + "\n" +
            "VPC: "+noncompliantVPC ) 
        
        msg = {
            "channel": "#{}".format(channel),
            "username": "WEBHOOK_USERNAME",
            "text": md_text,
            "icon_emoji": ":white_check_mark:"
        }
        
        encoded_msg = json.dumps(msg).encode('utf-8')
        resp = http.request('POST',url, body=encoded_msg)
        print({
            "message": md_text, 
            "status_code": resp.status, 
            "response": resp.data
        })
    except Exception as e:
        print('trying to send to slack failed')

        print(e)
        raise
    # ==== Slack END ===

    

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
