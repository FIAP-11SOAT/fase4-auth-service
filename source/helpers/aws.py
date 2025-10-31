import boto3
import orjson


def get_aws_secrets(secret_name: str) -> dict:
    client = boto3.client('secretsmanager')
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return orjson.loads(secret)
    except Exception as e:
        raise e
