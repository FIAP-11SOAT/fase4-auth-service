import aioboto3
import orjson


async def get_aws_secrets(secret_name: str) -> dict:
    session = aioboto3.Session()
    async with session.client("secretsmanager") as client:
        get_secret_value_response = await client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return orjson.loads(secret)
