# Workshop Guide: Event-Driven Image Processing

## Pre-Setup Instructions
1. Ensure AWS account with free tier.
2. Request Bedrock model access if doing GenAI extension.
3. Run `./build.sh` to package Lambda code and upload to hosted S3 bucket.
4. Deploy CloudFormation stack using the provided deploy command.

## Hands-on Steps
1. Upload images to the input S3 bucket to trigger initial metadata capture.
2. Enable the resize EventBridge rule to add image processing.
3. Uncomment and enable the caption rule for AI captioning.
4. Experiment with extending the pipeline (e.g., add watermarking, format conversion).
5. Monitor the event flow with CloudWatch and EventBridge.

## Test Deployment Instructions

For testing changes to the Lambda code:

1. Run `./build.sh` to package and upload updated Lambda code (requires `prodartifacts` AWS profile).
2. Manually empty the S3 buckets created by the stack (input, output buckets) to allow stack deletion.
3. Delete the CloudFormation stack: `aws cloudformation delete-stack --stack-name edip --profile sandbox`
4. Redeploy the stack: `aws cloudformation deploy --template-file src/templates/cloudformation.yaml --stack-name edip --profile sandbox --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM`

This process ensures the Lambda package is updated, as CloudFormation may not detect changes in S3-hosted code.

## Troubleshooting
- Check CloudWatch logs for each Lambda function.
- Verify IAM permissions and EventBridge rules.
- Ensure rules are enabled for the desired processing phases.
- Check DynamoDB for metadata updates.
- Monitor EventBridge for event delivery.