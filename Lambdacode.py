
import boto3
import time

sm_client = boto3.client("sagemaker")

def lambda_handler(event, context):

    print("FULL EVENT:", event)

    # Extract model package ARN
    model_package_arn = event["detail"]["ModelPackageArn"]
    print("Model ARN:", model_package_arn)

    # Naming
    timestamp = int(time.time())

    model_name = f"placement-model-{timestamp}"
    endpoint_config_name = f"placement-config-{timestamp}"
    endpoint_name = "placement-endpoint"

    try:
        # -------------------------
        # Create Model
        # -------------------------
        sm_client.create_model(
            ModelName=model_name,
            ExecutionRoleArn="arn:aws:iam::218736973000:role/service-role/AmazonSageMaker-ExecutionRole-20260209T120967",
            PrimaryContainer={
                "ModelPackageName": model_package_arn
            }
        )
        print("Model created")

        # Create Endpoint Config
        sm_client.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=[
                {
                    "VariantName": "AllTraffic",
                    "ModelName": model_name,
                    "InstanceType": "ml.m5.large",
                    "InitialInstanceCount": 1
                }
            ]
        )
        print("Endpoint config created")

        # Create or Update Endpoint
        try:
            sm_client.describe_endpoint(EndpointName=endpoint_name)

            print("Updating endpoint...")
            sm_client.update_endpoint(
                EndpointName=endpoint_name,
                EndpointConfigName=endpoint_config_name
            )

        except sm_client.exceptions.ClientError:
            print("Creating endpoint...")
            sm_client.create_endpoint(
                EndpointName=endpoint_name,
                EndpointConfigName=endpoint_config_name
            )

    except Exception as e:
        print("ERROR:", str(e))
        raise e

    return "Deployment triggered"
