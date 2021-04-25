This file is the complete documentation on how our cloud formation templates work along with
resources to AWS documentation explaining the syntax for each resource.

# enable-default-serverside-s3-bucket-encryption.yaml
This cloud formation template creates 5 resources
- S3BucketEncryptedCheckPermission (Lambda permissions)
- S3BucketEncryptedCheck (Lambda function)
- S3BucketEncryptedCheckConfigRule (Config Rule)
- LambdaExecutionRole (Execution Role)
- BasicS3EncryptionRole (Policy)

## The basic outline for how this template works
The config rule, which has permission to invoke the lambda function 'S3BucketEncryptedCheck', 
calls on the lambda function to execute the remediation. The lambda function 
has an execution role which only allows 6 function calls to be made. 
These functions are identified inside the policy associated with the execution role.

## How are these resources linked together
1. Config rule triggers lambda function.

## Links to the AWS documents on how to use the correct syntax
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html

# enable-auto-vpc-flowlogging.yaml
This cloud formation template creates 5 resources
- VPCFlowLogsEnabledCheckPermission (Lambda permissions)
- VPCFlowLogsEnabledCheck (Lambda function)
- VPCFlowLogsEnabledConfigRule (Config Rule)
- LambdaExecutionRole (Execution Role)
- BasicVPCFlowLogRole (Policy)

## The basic outline for how this template works
The config rule, which has permission to invoke the lambda function 'VPCFlowLogsEnabledCheck', 
calls on the lambda function to execute the remediation. The lambda function 
has an execution role which only allows 7 function calls to be made. 
These functions are identified inside the policy associated with the execution role.

## How are these resources linked together
1. Config rule triggers lambda function.

## Links to the AWS documents on how to use the correct syntax
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html

# enable-critical-monitoring.yaml
This cloud formation template creates 20 resources which are split into the following
- 3 resources made for stopping an EC2 instance
  - StopEC2Instance (Lambda function)
  - LambdaExecutionRoleStopEC2Instance (Execution Role)
  - BasicStopEC2InstanceRole (Policy)
- 3 resources made for blocking an IP address in an EC2 instance
  - EC2BlockIPAddress (Lambda function)
  - LambdaExecutionRoleEC2BlockIPAddress (Execution Role)
  - BasicStopEC2InstanceRole (Policy)
- 10 resources made to send GuardDuty logs to Slack
  - GuardDutyToSlackPermission (Lambda permissions)
  - GuardDutyToSlack (Lambda function)
  - GuardDutyToSlackVersion (Lambda version)
  - GuardDutyToSlackDestination (Lambda destinations)
  - LambdaExecutionRoleGuardDutyToSlack (Execution role)
  - BasicGuardDutyToSlackPolicy (Policy)
  - GuardDutyToSlackRule (Events rule to trigger lambda function)
  - GuardDutyToSlackSNS (AWS SNS)
  - GuardDutyToSlackSNSPolicy (Policy)
  - GuardDutyToSlackSNSSubscriptions (SNS Subscriptions)
- and 4 resources used to create the ChatBot in the Slack channel
  - GuardDutyToSlackChatBot (AWS Chatbot)
  - GuardDutyToSlackChatBotExecutionRole (Execution Role)
  - ChatBotNotificationsPolicy (Policy)
  - ChatBotLambdaPolicy (Policy)

## The basic outline for how this template works
For stopping an EC2 instance
- A lambda function is created with an execution role which only allows 
  4 function calls to be made. These functions are identified inside the policy 
  associated with the execution role.

For blocking an IP address on an EC2 instance
- A lambda function is created with an execution role which only allows 
  6 function calls to be made. These functions are identified inside the policy 
  associated with the execution role.

GuardDuty to Slack Notifications
- A lambda function is created with an execution role. The trigger for this lambda function
  is an event rule which looks for a specific event in Guard Duty. Once the lambda function
  is invoked, two async invocations are made to SNS, which sends out a message in Slack.

GuardDuty to Slack ChatBot
- A ChatBot is created using AWS ChatBot with an execution role which only allows
  5 function calls to be made. These policies are taken from AWS documents. In these
  documents, they are refered to as the AWS Chatbot Lambda-Invoke Command Permissions policy
  and the AWS Chatbot Notification Permissions IAM policy.

## How are these resources linked together
The remediation works as follows
1. GuardDuty to Slack Notifications waits for lambda function to be triggered.
2. SNS message is sent to Slack, giving out options for the user.
3. The user replies and this is picked up by the ChatBot.
4. Relevant functions is then called based on what option the user has chosen via. ChatBot. 

## Links to the AWS documents on how to use the correct syntax
### Stopping EC2 Instances links/Blocking IP address links
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
### GuardDuty to Slack Notification links
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html
### ChatBot links
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
- https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html