# How this lambda function works
# Lambda function takes one variable as the payload - the EC2 instance id.
# Using the instance id, we can stop the instance using the boto3 function stop_instances.
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html for more information
# on how this function works.
import json
import boto3
import botocore

ec2 = boto3.client('ec2')


def lambda_handler(event, context):
    instance_id = event['id']
    
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except botocore.exceptions.ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except botocore.exceptions.ClientError as e:
        print(e)
    
    
    return "succesfully stopped EC2 instance with instance id: " + instance_id
