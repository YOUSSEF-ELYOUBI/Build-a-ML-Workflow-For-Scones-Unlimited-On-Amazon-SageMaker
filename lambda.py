# serializeImageData
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Downloads an image from S3, base64 encodes it,
    and returns it. This version is robust to handle various
    Step Function input formats, including a stringified 'Payload'.
    """
    
    
    if "Payload" in event:
        # Check if the payload itself is a string that needs to be parsed.
        if isinstance(event["Payload"], str):
            actual_event = json.loads(event["Payload"])
        else:
            
            actual_event = event["Payload"]
    else:
        # If there's no 'Payload' key, the event is the input.
        actual_event = event
    
    
  
    key = actual_event['s3_key']
    bucket = actual_event['s3_bucket']

    download_path = "/tmp/image.png"
    s3.download_file(bucket, key, download_path)

    with open(download_path, "rb") as f:
        image_data_bytes = base64.b64encode(f.read())

    image_data_string = image_data_bytes.decode('utf-8')

    print(f"Successfully serialized image: s3://{bucket}/{key}")

    
    # direct JSON body, as Step Functions will handle the rest.
    return {
        "image_data": image_data_string,
        "s3_bucket": bucket,
        "s3_key": key,
        "inferences": []
    }

# classfication
import json
import base64
import boto3

ENDPOINT = 'image-classification-2025-08-19-17-31-02-103' # Use your actual endpoint name
runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    
     Check if the input is from a direct test or the Step Function
    if "body" in event and isinstance(event["body"], str):
        # Input is from a direct test, parse the body string
        body = json.loads(event["body"])
    else:
        # Input is from the Step Function, the event is already the body we need
        body = event
        
    # Now 'body' is guaranteed to be a dictionary
    image = base64.b64decode(body['image_data'])

    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType='image/png',
        Body=image
    )
    
    inferences_string = response['Body'].read().decode('utf-8')
    body['inferences'] = inferences_string
    
    return {
        'statusCode': 200,
        'body': json.dumps(body) 
    }
# filter 
# filter
import json

THRESHOLD = 0.7

def lambda_handler(event, context):
    
    # Robust Input Handling
    if "body" in event and isinstance(event["body"], str):
        body = json.loads(event["body"])
    else:
        body = event
        
    inferences = json.loads(body["inferences"]) 

    if max(inferences) <= THRESHOLD:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }