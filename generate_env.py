import boto3
import json


def fetch_secret(secret_name, region_name="us-east-1"):
    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        # Fetch the secret value
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)

        # Parse the secret string if it exists
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
            secret_dict = json.loads(secret)  # Convert to dictionary
            return secret_dict

        # Handle binary secrets if necessary
        else:
            decoded_binary_secret = get_secret_value_response["SecretBinary"]
            return json.loads(decoded_binary_secret)

    except Exception as e:
        print(f"Error fetching secret: {e}")
        return None


def lambda_handler(event, context):
    # Define the secret name
    secret_name = "rds!db-85f08615-c22b-4793-b8c4-f54ccce78620"
    secret_endpoint = "costanza/prod/endpoint"
    secret_port = "costanza/port/prod"
    # Fetch the secret
    secret = fetch_secret(secret_name)

    if secret:
        username = secret.get("username")
        password = secret.get("password")
        endpoint = secret.get("host")
        port = secret.get("port")
        endpoint = secret.get("endpoint")
        # Now you can use the username and password securely in your logic
        print(f"Username: {username}, Password: {password}")

    # Generate .env file content
    if secret:
        with open(".env", "w") as env_file:
            env_file.write(f"USERNAME={secret.get('username')}\n")
            env_file.write(f"PASSWORD={secret.get('password')}\n")

    return {"statusCode": 200, "body": "Secrets fetched successfully"}
