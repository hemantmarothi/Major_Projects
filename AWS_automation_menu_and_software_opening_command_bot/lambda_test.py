import boto3
import json

def lambda_handler(event, context):
    # Extract parameters from the event
    s3_bucket = event.get('s3_bucket')
    file_name = event.get('file_name')

    # Initialize S3 client
    s3_client = boto3.client('s3')
    try:
        # Read the content of the file from S3
        response = s3_client.get_object(Bucket=s3_bucket, Key=file_name)
        file_content = response['Body'].read().decode('utf-8')

        # Print the content to CloudWatch Logs
        print(f"Content of {file_name} in {s3_bucket}:\n{file_content}")

        return {
            'statusCode': 200,
            'body': json.dumps('File content printed successfully!')
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {e}")
        }
