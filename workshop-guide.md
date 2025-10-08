# Workshop Guide: Event-Driven Image Processing

## 📦 Part 0 - Deploying the Stack

Before we begin, we need to deploy the CloudFormation stack that sets up all necessary resources.

1. Logon to your AWS account. Ensure that you are in the `us-east-1` region.

2. Open the CloudFormation console.

3. Click "Create stack" > "With new resources (standard)".

4. Under "Specify template", select "Amazon S3 URL".

5. Enter the URL to the CloudFormation template:
   ```
    https://ssennett-lab-persistent.s3.amazonaws.com/2025/eventdrivenimageprocessing/cloudformation.yaml
   ```

6. Click "Next".

7. On the "Specify stack details" page, enter a unique name for the stack.

8. Click "Next".

9. On the "Configure stack options" page, check the box for "I acknowledge that AWS CloudFormation might create IAM resources with custom names".

10 . Click "Next".

11. On the "Review" page, review the settings and click "Create stack".

12. Wait for the stack status to change to "CREATE_COMPLETE". (aprx 2 minutes)

13. Confirm that all 15 resources have been created successfully.

The **Resources** tab will help you locate all the resources used in this workshop.

## 📝 Part 1 - Initial Processing

Let's see how the initial image processing works. 

1. Open the **MetadataTable** (DynamoDB) and **InputBucket** (S3) resources in separate tabs.

2. In the DynamoDB console, click on the **Items** tab to view the table contents.

3. In the S3 console, click on the **Objects** tab of the **InputBucket**.

4. Click the **Upload** button.

5. Select and upload a test image from your local machine
    > *Note*: Test images can be found in the `./test-images` folder of the GitHub repository.

6. Note that nothing has changed in the DynamoDB table yet. This is because the EventBridge rule that triggers the initial metadata capture is disabled by default.

7. In the S3 console, click on the **Properties** tab of the **InputBucket**.

8. Scroll to the **Amazon EventBridge** section and click **Edit**.

9. Toggle the switch to **Enabled** and click **Save changes**.

10. In the S3 console, click on the **Objects** tab of the **InputBucket** again.

11. Upload another test image from your local machine.

12. Observe the DynamoDB table. You should see a new item added with metadata about the uploaded image.

## 📸 Part 2 - Resizing Images

Now that we have the initial metadata capture working, let's add image resizing to the pipeline. The Lambda function has already been created, but the EventBridge rule that triggers it is disabled by default.

1. Open the **ResizeRule** resource in the EventBridge console.

2. Click the **Enable** button to enable the rule.

3. In the S3 console, click on the **Objects** tab of the **InputBucket**.

4. Upload another test image from your local machine.

4. Open the **OutputBucket** resource in the S3 console.

6. You should see a new object added with the resized image under the `processed/` key.

7. In the DynamoDB console, you should see the metadata for the uploaded image updated with the new resized image information.

## 🤖 Part 3 - Adding AI Captions

Finally, we're going to enable smart captioning with AI. This step requires access to Bedrock models. If you don't have access, you can skip this part, or [enable AI model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access-modify.html), specifically to Anthropic Claude 3.5 Sonnet in `us-east-1`.

Instead of enabling an existing rule, we will take the next step and configure the rule manually.

1. Open the EventBridge console.

2. Click on **Rules** in the left-hand menu.

3. Click the **Create rule** button.

4. Enter `CaptionRule` as the rule name.

5. Ensure the Event bus is set to `default`.

6. Set the rule type to **Rule with an event pattern**.

7. Ensure the Event source is set to **Other**, since we are using custom events.

8. Enter the following event pattern:
   ```json
    {
        "source": ["edipworkshop.image.processor"],
        "detail-type": ["Processing Complete"]
    }
   ```

9. Click **Next**.

10. Set the target to **Lambda function**.

11. Select the **{stackName}-edip-caption-processor** from the function dropdown.

12. Uncheck the box for **Use execution role (recommended)**.

13. Click **Next**.

14. Click **Next** to skip the tags page.

15. Review the settings and click **Create rule**.

## 🔈 Part 4 - Custom Integration (Polly for Audio Captions)

Now, it's time to experiment!

Build an AWS Lambda Function to listen for events from EventBridge and use Amazon Polly to generate audio captions for images. Note that you can accomplish this without modifying any existing code, only adding new code.

Happy clouding!
