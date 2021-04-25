import boto3
import hashlib
import json
from botocore.exceptions import ClientError
import urllib3
http = urllib3.PoolManager()

# ID of the security group we want to update
# SECURITY_GROUP_ID = "sg-XXXX"

# Description of the security rule we want to replace
# SECURITY_RULE_DESCR = "My Home IP"
    
def gen_iprange(ip_addr, i = 32):
    if(ip_addr.find("/") == -1): # hash not found
        # i - Cisco style mark (or whatever it's called)
        #  * 32 means to specify 1 IP address only
        #  * 24 means to specify the entire subnet (e.g. 192.168.10.* )
        #  * 0 means to block the entire IPv4 range ie the internet (lol)
        #  Too sleepy to remember the name for the thing, but it's calculated as,
        #  `2^(32-i)` many IPv4 addresses (to specify) 
        buf = "{:s}/{:d}".format(ip_addr, i)
    else:
        buf = ip_addr
    
    return buf
    
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    vpc = ec2.describe_instances(
        InstanceIds=[
            event['id']
        ],
    )['Reservations'][0]['Instances'][0]['VpcId']
    print(vpc)
    
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
