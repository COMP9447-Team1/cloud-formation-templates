import json
import boto3
client = boto3.client('cloudformation')

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('lambda')
    role_response = (client.get_function_configuration(
        FunctionName = os.environ['AWS_LAMBDA_FUNCTION_NAME'])
    )
    print(role_response)
    roleArn = role_response['Role']
    accountId = context.invoked_function_arn.split(":")[4]
    commandType = event['id']
    capabilities = ['CAPABILITY_IAM']
    stackName = commandType
    print(commandType)
    templateUrl = f"https://remediation-cfns-{accountId}.s3.amazonaws.com/{commandType}.yaml"
    print(templateUrl)
    print(event)
    print(context)

    response = client.create_stack(
        StackName=stackName,
        TemplateURL=templateUrl,
        Capabilities=capabilities,
        RoleARN=roleArn,
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }