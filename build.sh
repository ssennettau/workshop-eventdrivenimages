#!/bin/sh
# Builds and uploads the artifacts for the backend S3 repository.
# Not required for workshop usage - hosting only.

set -e

# Lambda Packages
rm ./dist/lambdapackage.zip >/dev/null 2>&1 || true
cd ./src/lambda
zip \
    ./../../dist/lambdapackage.zip \
    ./* >/dev/null
cd ../../
aws s3 cp \
    ./dist/lambdapackage.zip \
    s3://ssennett-lab-persistent/2025/eventdrivenimageprocessing/lambdapackage.zip \
    --profile labartifacts >/dev/null
echo "📦 Lambda Package Uploaded > https://ssennett-lab-persistent.s3.amazonaws.com/2025/eventdrivenimageprocessing/lambdapackage.zip"

# CloudFormation Template
aws s3 cp \
    ./src/templates/cloudformation.yaml \
    s3://ssennett-lab-persistent/2025/eventdrivenimageprocessing/cloudformation.yaml \
    --profile labartifacts >/dev/null
echo "🛠️ CloudFormation Template Uploaded > https://ssennett-lab-persistent.s3.amazonaws.com/2025/eventdrivenimageprocessing/cloudformation.yaml"

echo "✅ Deployment complete."
