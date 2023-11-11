import boto3
import redis
import json
# Initialize SQS and Redis clients
sqs = boto3.client('sqs')
redis_client = redis.StrictRedis(host='guard.flycqz.clustercfg.use2.cache.amazonaws.com:6379', port=6379, db=0)

def lambda_handler(event, context):
    # Receive messages from SQS
    print(json.dumps(event))
    queue_url = 'https://sqs.us-east-2.amazonaws.com/746454863131/guarddutyfinding'
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'All'
        ],
        MessageAttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=10,
        VisibilityTimeout=30,
        WaitTimeSeconds=0
    )

    # Store messages in Redis
    for message in response.get('Messages', []):
        body = message['Body']
        redis_client.set(message['MessageId'], body)

    return {
        'statusCode': 200,
        'body': 'Messages stored in Redis'
    }
