import os
from dotenv import load_dotenv
import boto3
import json


def fetch_aws_secrets(secret_name, region_name="us-east-1"):
    """Fetch secrets from AWS Secrets Manager."""
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret = response["SecretString"]
            return json.loads(secret)
        else:
            decoded_binary_secret = response["SecretBinary"]
            return json.loads(decoded_binary_secret)

    except Exception as e:
        print(f"Failed to fetch secrets: {e}")
        return None


def load_config():
    """Loads environment variables based on the environment."""
    environment = os.getenv("ENVIRONMENT", "local")

    if environment == "local":
        # Load local environment variables from .env.local
        load_dotenv(".env.local")
        print("Loaded local environment variables")
    elif environment == "production":
        # Fetch secrets from AWS Secrets Manager
        secret_name = "rds!db-85f08615-c22b-4793-b8c4-f54ccce78620"
        secrets = fetch_aws_secrets(secret_name)
        if secrets:
            os.environ.update(secrets)
        print("Loaded production environment variables from AWS Secrets Manager")


load_config()
