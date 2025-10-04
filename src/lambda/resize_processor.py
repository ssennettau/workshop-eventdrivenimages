import boto3
import json
import os
from PIL import Image
import io
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
events = boto3.client('events')

INPUT_BUCKET = os.environ['INPUT_BUCKET']
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
TABLE_NAME = os.environ['TABLE_NAME']
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'default')

def lambda_handler(event, context):
    # Parse S3 event
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        if bucket != INPUT_BUCKET:
            continue

        try:
            # Download image
            response = s3.get_object(Bucket=bucket, Key=key)
            image_data = response['Body'].read()

            # Process image (resize to thumbnail)
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((200, 200))
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='JPEG')
            output_data = output_buffer.getvalue()

            # Upload processed image
            output_key = f"processed/{key}"
            s3.put_object(Bucket=OUTPUT_BUCKET, Key=output_key, Body=output_data, ContentType='image/jpeg')

            # Store metadata
            table = dynamodb.Table(TABLE_NAME)
            table.put_item(Item={
                'id': key,
                'original_size': len(image_data),
                'processed_size': len(output_data),
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'success'
            })

            # Emit event for optional captioning
            events.put_events(
                Entries=[{
                    'EventBusName': EVENT_BUS_NAME,
                    'Source': 'image.processor',
                    'DetailType': 'Processing Complete',
                    'Detail': json.dumps({
                        'image_key': key,
                        'processed_key': output_key
                    })
                }]
            )

            print(f"Processed {key} successfully")

        except Exception as e:
            print(f"Error processing {key}: {str(e)}")
            # Log error (could add to DynamoDB or CloudWatch)