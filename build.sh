#!/bin/sh
# Builds and uploads the artifacts for the backend S3 repository.
# Not required for workshop usage - hosting only.

set -e

echo "🛠️ Deploying artifacts to S3..."

# Lambda Packages
cd ./src/lambda
zip \
    ./../../dist/lambdapackage.zip \
    ./*
cd ../../
aws s3 cp \
    ./dist/lambdapackage.zip \
    s3://ssennett-lab-persistent/2025/eventdrivenimageprocessing/lambdapackage.zip \
    --profile labartifacts

# CloudFormation Template
aws s3 cp \
    ./src/templates/cloudformation.yaml \
    s3://ssennett-lab-persistent/2025/eventdrivenimageprocessing/cloudformation.yaml \
    --profile labartifacts

echo "✅ Deployment complete."
