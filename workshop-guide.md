# Workshop Guide: Event-Driven Image Processing

## Pre-Setup Instructions
1. Ensure AWS account with free tier.
2. Request Bedrock model access if doing GenAI extension.
3. Run `./build.sh` to package Lambda code and upload to hosted S3 bucket.
4. Deploy CloudFormation stack using src/templates/cloudformation.yaml.

## Hands-on Steps
1. Deploy UI to S3.
2. Configure EventBridge.
3. Test upload and processing.
4. Add observability.
5. Optional: GenAI captioning.

## Test Deployment Instructions

For testing changes to the Lambda code:

1. Run `./build.sh` to package and upload updated Lambda code (requires `prodartifacts` AWS profile).
2. Manually empty the S3 buckets created by the stack (input, output, ui buckets) to allow stack deletion.
3. Delete the CloudFormation stack: `aws cloudformation delete-stack --stack-name edip --profile sandbox`
4. Redeploy the stack: `aws cloudformation deploy --template-file src/templates/cloudformation.yaml --stack-name edip --profile sandbox --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM`

This process ensures the Lambda package is updated, as CloudFormation may not detect changes in S3-hosted code.

## Troubleshooting
- Check CloudWatch logs for errors.
- Verify IAM permissions.
- Ensure EventBridge rules are active.