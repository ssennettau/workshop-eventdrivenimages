# Event-Driven Image Processing Workshop

## Description

This workshop introduces Event-Driven Architecture (EDA) using AWS services. Participants will build a serverless image processing pipeline with three phases: initial metadata capture on upload, optional resizing, and optional AI captioning. The focus is on configuring event flows, monitoring, and understanding EDA principles with extensibility for experimentation.

Key learning outcomes:
- Configure AWS EventBridge for event routing
- Implement serverless processing with Lambda
- Monitor event-driven systems with CloudWatch
- Explore optional AI integration with Amazon Bedrock
- Design extensible event-driven architectures

## Architecture

```mermaid
graph TD
    A[S3 Upload] -->|Object Created| B[EventBridge]
    B -->|S3 Event| C[Initial Lambda]
    C -->|Store Metadata| D[DynamoDB Table]
    C -->|Image Uploaded Event| E[EventBridge]
    E -->|Resize Rule (Disabled)| F[Resize Lambda]
    F -->|Process & Update| D
    F -->|Processing Complete| G[EventBridge]
    G -->|Caption Rule (Commented)| H[Caption Lambda]
    H -->|AI Caption| D
    F -->|Store Processed| I[S3 Output Bucket]
    J[CloudWatch] -->|Metrics/Logs| C
    J -->|Metrics/Logs| F
    J -->|Metrics/Logs| H
```

## Prerequisites

- AWS account with free tier access
- Basic familiarity with AWS console (IAM, S3, Lambda, EventBridge)
- AWS CLI configured for deployment
- Optional: Bedrock model access for GenAI extension

## Target Audience

- 200-level workshop: Assumes basic AWS knowledge, introduces EDA concepts
- Developers, architects, or IT professionals new to event-driven patterns
- No prior EDA experience required, but AWS fundamentals helpful

## Getting Started

1. Clone this repository
2. Run `./build.sh` to package and upload Lambda functions
3. Deploy CloudFormation stack: `aws cloudformation deploy --template-file src/templates/cloudformation.yaml --stack-name edip --profile sandbox --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM`
4. Upload images to the input S3 bucket to trigger processing
5. Follow the workshop guide in `workshop-guide.md` for extensions

## Resources

- [Workshop Plan](workshop-plan.md)
- [Workshop Guide](workshop-guide.md)
- [Test Plan](specs/workshop/test-plan.md)
