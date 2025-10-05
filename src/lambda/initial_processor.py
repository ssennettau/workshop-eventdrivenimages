import boto3
import json
import os
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
events = boto3.client('events')

INPUT_BUCKET = os.environ['INPUT_BUCKET']
TABLE_NAME = os.environ['TABLE_NAME']
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'default')

def lambda_handler(event, context):
    # Parse EventBridge S3 event
    detail = event['detail']
    bucket = detail['bucket']['name']
    key = detail['object']['key']

    if bucket != INPUT_BUCKET:
        return

    try:
        # Get image metadata
        response = s3.head_object(Bucket=bucket, Key=key)
        original_size = response['ContentLength']

        # Store initial metadata
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item={
            'id': key,
            'original_size': original_size,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'uploaded'
        })

        # Emit event for resizing
        events.put_events(
            Entries=[{
                'EventBusName': EVENT_BUS_NAME,
                'Source': 'edipworkshop.image.processor',
                'DetailType': 'Image Uploaded',
                'Detail': json.dumps({
                    'image_key': key
                })
            }]
        )

        print(f"Initial metadata stored for {key}")

    except Exception as e:
        print(f"Error processing {key}: {str(e)}")