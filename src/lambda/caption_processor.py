import boto3
import json
import os
import base64

bedrock = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')

OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
TABLE_NAME = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    for record in event['Records']:
        detail = json.loads(record['detail'])
        image_key = detail['image_key']

        try:
            # Get processed image from S3
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=OUTPUT_BUCKET, Key=f"processed/{image_key}")
            image_data = response['Body'].read()

            # Encode to base64 for Bedrock
            image_b64 = base64.b64encode(image_data).decode('utf-8')

            # Call Bedrock for caption
            response = bedrock.invoke_model(
                modelId='amazon.titan-image-generator-v1',  # Adjust for vision model
                body=json.dumps({
                    'inputText': 'Describe this image in a short caption.',
                    'image': image_b64
                })
            )

            result = json.loads(response['body'].read())
            caption = result.get('caption', 'No caption generated')

            # Update metadata
            table = dynamodb.Table(TABLE_NAME)
            table.update_item(
                Key={'id': image_key},
                UpdateExpression='SET caption = :c',
                ExpressionAttributeValues={':c': caption}
            )

            print(f"Captioned {image_key}: {caption}")

        except Exception as e:
            print(f"Error captioning {image_key}: {str(e)}")