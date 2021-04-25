# How this lambda function works
# Lambda function takes two variables as the payload - the EC2 instance id and the IP address to block.
# Using the instance id, we need to find the network ACL which this instance uses.
# this is because the network ACL defines inbound and outbound rules aka.
# what is allowed to use this instance and what is allowed to come out of this instance
# We do this by using the instance Id to get the Vpc id, and then using the Vpc id to get the network ACL id.
# From here, we create a new inbound rule. 
# Most of these function calls are made from boto3. 
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html for more information
# on how each function works.

import boto3
import hashlib
import json
from botocore.exceptions import ClientError
import urllib3
http = urllib3.PoolManager()

# function looks to see if IP subnet is given 
# i.e. checks to see if there is a "/" in the given IP address
# if no "/" is given, then we assume that only a single IP address is to be blocked 
# i.e. adding a /32 to the end of the IP address
def gen_iprange(ip_addr, i = 32):
    if(ip_addr.find("/") == -1): # hash not found
        buf = "{:s}/{:d}".format(ip_addr, i)
    else:
        buf = ip_addr
    
    return buf
    
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # using the given instance id, find the associated VPC id.
    vpc = ec2.describe_instances(
        InstanceIds=[
            event['id']
        ],
    )['Reservations'][0]['Instances'][0]['VpcId']
    print(vpc)
    
    # using the given VPC id, find the associated network ACL id.
    networkACL = ec2.describe_network_acls(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpc,
                ]
            },
        ],
    )['NetworkAcls'][0]['Associations'][0]['NetworkAclId']
    print(networkACL)
    
    # finding out how many inbound and outbound rules are already
    # made in the given network ACL
    entryCount = len(ec2.describe_network_acls(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpc,
                ]
            },
        ],
    )['NetworkAcls'][0]['Entries'])
    
    # randomising the rule number, making sure that theres enough space
    # between rule numbers to add more rules later on if needed (hence multiplying it by 5)
    # we do this because the rule number needs to be unique.
    # by default, the only rule number used in a network ACL is 100.
    ruleNum = entryCount*5
    
    ingress = ec2.create_network_acl_entry(
        CidrBlock=gen_iprange(event['ip']),
        Egress=False,
        NetworkAclId=networkACL,
        Protocol='-1',
        RuleAction='deny',
        RuleNumber=ruleNum,
    )
    
    # === Slack Notifications part ====
    try: #  try logic to catch errors
        
        # parameters
        channel = "{{INSERT_CHANNEL_NAME_HERE}}"
        url = "{{INSERT_WEBHOOK_HERE}}"
        
        # my own var
        md_text = "*\U0001F528 Ban Success*\n\n*" + gen_iprange(event['ip']) + "* has been banned."
        
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
        print(e)
        raise
    # ==== Slack END ===
    return "Successully blocked IP address."
