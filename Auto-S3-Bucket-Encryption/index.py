# How this lambda function works
# Lambda function is triggered by a config rule, which means that we're going to use the event variable instead of the context variable.
# We grab the relevant information from the event to use in our get_bucket_encryption and put_bucket_encryption calls.
# We start by using the bucket name to check if encryption is enabled on the bucket.
# If not, we add encryption on it.
# Most of these function calls are made from boto3. 
# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html for more information
# on how each function works.
import json
import boto3
import urllib3 
http = urllib3.PoolManager() # not sure not why inside of def - is it executed only once?

client = boto3.client('s3')
def lambda_handler(event, context):
    # TODO implement
    print("event", event)
    print("context", context)
        
    invokingEvent = json.loads(event["invokingEvent"])
    bucketOwner = invokingEvent['configurationItem']['awsAccountId']
    bucketName = invokingEvent['configurationItem']['resourceName']

    try:
        # TODO: write code...
        response = client.get_bucket_encryption(
            Bucket=bucketName,
            ExpectedBucketOwner=bucketOwner
        )
    except Exception as e:
        if ('ServerSideEncryptionConfigurationNotFoundError' in str(e)):
            print("enabling encryption")
            result = 'Server Side Encryption is now SUCCESSFULLY enabled for S3 Bucket ' + bucketName
            
            response = client.put_bucket_encryption(
                Bucket=bucketName,
                ServerSideEncryptionConfiguration={
                    'Rules': [
                        {
                            'ApplyServerSideEncryptionByDefault': {
                                'SSEAlgorithm': 'AES256'
                            },
                            'BucketKeyEnabled': True
                        },
                    ]
                },
                ExpectedBucketOwner=bucketOwner
            )
            
            print('yoooo', response)
        
            # === Slack Notifications part ====
            try: #  try logic to catch errors
                # parameters
                channel = "{{INSERT_CHANNEL_NAME_HERE}}"
                url = "{{INSERT_SLACK_WEBHOOK_HERE}}"
                
                # my own var
                md_text = "*"+( event.get('detail-type', "Config Rule") + "*\n\n" + result + "\n")
                
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
            print('did it work??', result)

    
        
    
    #val = (response['Rules']['BucketKeyEnabled'])
    #print(val)
    
    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
