# Event-Driven Image Processing Workshop Plan

## Workshop Title
Event-Driven Image Processing Workshop

## Objectives
- Introduce Event-Driven Architecture (EDA) using AWS EventBridge for extensibility.
- 200-level target: Assumes basic AWS knowledge (IAM, S3, Lambda); focuses on EDA design and configuration.
- Emphasize visual event flow tracking via basic web UI (no deep coding or tooling deployment).

## Core Components
- **Web UI**: Pre-built static site on S3 for image uploads and result visualization (no configuration required).
- **Event Ingestion**: S3 bucket events routed to EventBridge.
- **Processing Pipeline**: EventBridge rules trigger Lambda functions for image processing.
- **Storage**: Processed images in S3, metadata in DynamoDB.
- **Notification**: SNS for completion alerts.

## Architecture Overview
- User uploads image via web UI to S3 input bucket.
- S3 sends event to EventBridge.
- EventBridge rule matches and triggers resize Lambda (processes image, stores thumbnail in output S3, logs metadata in DynamoDB).
- Optional: Resize Lambda emits 'processing_complete' event; optional rule triggers GenAI captioning Lambda (calls Bedrock for alt text, stores in metadata).
- Observability: CloudWatch metrics (event counts, latency, success/failure), structured logs, custom dashboards.
- UI displays processed images and optional captions for event flow visualization.

## Hands-on Activities (Focus on EDA Configuration)
1. Deploy pre-built web UI to S3 and set up core AWS resources (buckets, DynamoDB, SNS, IAM).
2. Create EventBridge bus and rules for S3 upload events.
3. Configure rules to trigger Lambda processing functions.
4. Test event-driven flows via web UI uploads.
5. Add observability: Set up CloudWatch metrics, logs, and dashboards; demonstrate monitoring successes/failures and debugging via logs.
6. Optional Extension: Enable GenAI captioning (request Bedrock access, add optional rule/Lambda).

## Prerequisites
- AWS account with free tier access.
- Basic AWS knowledge (IAM, S3, Lambda).
- EDA concepts introduced (EventBridge rules/patterns, event decoupling).
- Internet access for web UI and console.

## Value-Adds (Differentiating from Standard EDA Workshops)
- **GenAI Integration**: Optional microservice for image captioning using Bedrock (topical, unique use case; demonstrates advanced chaining).
- **Observability Focus**: Hands-on CloudWatch setup; emphasizes monitoring distributed event systems (success/failure rates, logs for error debugging).

## Alignment with Project Principles
- **Simplicity**: Pre-built components, console-based setup, no coding required.
- **Modularity**: Decoupled Lambdas and events; optional extensions as separate microservices.
- **Ease in Heterogeneous Environments**: All cloud-based; web UI and console work across platforms/devices.

## Estimated Duration
2-3 hours (core flow + observability; GenAI as optional add-on).

## Target Audience Fit
200-level - Builds on AWS basics, introduces EDA without overwhelming complexity. Push back if additions exceed time/basics.