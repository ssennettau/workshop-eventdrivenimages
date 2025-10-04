# Workshop Guide: Event-Driven Image Processing

## Pre-Setup Instructions
1. Ensure AWS account with free tier.
2. Request Bedrock model access if doing GenAI extension.
3. Package Lambda code: zip resize_processor.py and caption_processor.py, upload to S3 bucket.
4. Deploy CloudFormation stack using src/templates/cloudformation.yaml.

## Hands-on Steps
1. Deploy UI to S3.
2. Configure EventBridge.
3. Test upload and processing.
4. Add observability.
5. Optional: GenAI captioning.

## Troubleshooting
- Check CloudWatch logs for errors.
- Verify IAM permissions.
- Ensure EventBridge rules are active.