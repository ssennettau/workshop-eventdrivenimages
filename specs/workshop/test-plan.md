# Test Plan for Workshop

## End-to-End Test Flow
1. Deploy resources using deploy.sh
2. Upload UI to S3 bucket and enable static hosting
3. Create Lambda functions with code
4. Set up EventBridge rules
5. Upload test image via UI
6. Verify processing: Check output S3, DynamoDB, logs
7. Test observability: View CloudWatch metrics/dashboards
8. Optional: Enable captioning, test Bedrock integration

## Validation Checks
- Image upload triggers event
- Processing completes successfully
- Metadata stored correctly
- UI displays results
- Metrics show processing stats
- Logs detail successes/failures