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
    # Parse EventBridge S3 event
    detail = event['detail']
    bucket = detail['bucket']
    key = detail['object']['key']

    if bucket != INPUT_BUCKET:
        return

    try:
        # Download image
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()

        # Process image (resize to 200x200 JPG)
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('RGB')
        image = image.resize((200, 200))
        output_buffer = io.BytesIO()
        image.save(output_buffer, format='JPEG')
        output_data = output_buffer.getvalue()

        # Upload processed image
        output_key = f"processed/{key}"
        s3.put_object(Bucket=OUTPUT_BUCKET, Key=output_key, Body=output_data, ContentType='image/jpeg')

        # Update metadata
        table = dynamodb.Table(TABLE_NAME)
        table.update_item(
            Key={'id': key},
            UpdateExpression='SET processed_size = :ps, #s = :st',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':ps': len(output_data), ':st': 'processed'}
        )

        # Emit event for optional captioning
        events.put_events(
            Entries=[{
                'EventBusName': EVENT_BUS_NAME,
                'Source': 'edipworkshop.image.processor',
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
