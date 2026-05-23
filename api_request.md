# Making Your First API Request to AWS Bedrock

To make your first API request to AWS Bedrock, you need three essential components:

1. A Bedrock Runtime Client
2. A Model ID (or Inference Profile ID)
3. A User Message

---
[reference code](aws_bedrock_api_request.ipynb)
# 1. Setting Up the Bedrock Client

Start by creating a Bedrock Runtime client using `boto3`.

```python
import boto3

client = boto3.client(
    "bedrock-runtime",
    region_name="us-west-2"
)
```
The region_name specifies which AWS region your request is sent from.


# 2. Understanding Model IDs and Regional Availability

Not every Bedrock model is available in every AWS region.

For example:
```
A model may exist in us-west-2

But not in us-east-1
```
If you try to call a model from a region where it is unavailable, AWS returns an error similar to:

The provided model identifier is invalid.

or

Model does not exist.

This can be confusing because the model itself exists — just not in your selected region.

# 3. Using Inference Profiles

Inference Profiles solve regional availability problems.

Instead of calling the raw model ID directly, you can use an inference profile ID that automatically routes requests to a supported region.

Benefits:

No need to track model availability manually
Automatic cross-region routing
Easier production deployments

Example:
```
model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
```
When using this inference profile:

Your request can originate from one region
AWS routes it to another region where the model is actually hosted
# 4. Finding Inference Profile IDs

To find inference profile IDs:

Open the AWS Bedrock Console
Navigate to:
Cross-region inference
Select your desired model
Copy the Inference Profile ID

Important:

Do NOT copy the model ID from the main model catalog page if you want cross-region support.

# 5. Creating User Messages

Bedrock messages use a structured format.

Example:
```
user_message = {
    "role": "user",
    "content": [
        {
            "text": "What's 1+1?"
        }
    ]
}
```
Why is content a list?

Because Bedrock supports multimodal inputs.

A single message can contain:

Text
Images
Other media types

This structure allows future expansion for multimodal AI applications.

# 6. Making Your First Request

Use the converse() method to send messages to the model.
```
response = client.converse(
    modelId=model_id,
    messages=[user_message]
)
```
# 7. Reading the Response

The response object contains metadata and generated content.

To extract the generated text:
```
response["output"]["message"]["content"][0]["text"]
```
Example:
```
print(response["output"]["message"]["content"][0]["text"])
```
# 8. Understanding Message Types

Bedrock conversations use two primary message roles:

User Messages
```
Messages sent by you:

{
    "role": "user",
    "content": [
        {"text": "Hello"}
    ]
}
```
Assistant Messages

Messages returned by the model:
```
{
    "role": "assistant",
    "content": [
        {"text": "Hi! How can I help you today?"}
    ]
}
```
Both message types use the same structure:

role
content

This consistent format makes it easy to build multi-turn conversations.