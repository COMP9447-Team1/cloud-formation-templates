import json
import boto3
client = boto3.client('cloudformation')

def lambda_handler(event, context):
    # TODO implement
    stackName = event["id"]
    print(stackName)
    capabilities = ['CAPABILITY_IAM']
    client = boto3.client('lambda')
    role_response = (client.get_function_configuration(
        FunctionName = os.environ['AWS_LAMBDA_FUNCTION_NAME'])
    )
    print(role_response)
    roleArn = role_response['Role']
    resourceTypes = ['AWS::*']
    
    
    response = client.delete_stack(
        StackName=stackName,
        RoleARN=roleArn
    )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }