from contextlib import asynccontextmanager

import aioboto3
from boto3.dynamodb.conditions import Key


class AsyncDatabaseRepository:
    def __init__(self, table_name, region_name='us-east-1'):
        self.table_name = table_name
        self.region_name = region_name
        self.session = aioboto3.Session()

    async def create_table_if_not_exists(self):
        async with self.session.resource('dynamodb', region_name=self.region_name) as dynamodb:
            existing_tables = []
            async for table in dynamodb.tables.all():
                existing_tables.append(table.name)

            if self.table_name in existing_tables:
                return False

            table = await dynamodb.create_table(
                TableName=self.table_name,
                BillingMode='PAY_PER_REQUEST',
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'tax_id', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'TaxIDIndex',
                        'KeySchema': [
                            {'AttributeName': 'tax_id', 'KeyType': 'HASH'}
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        }
                    }
                ],
            )
            return True

    @asynccontextmanager
    async def get_table(self):
        async with self.session.resource('dynamodb', region_name=self.region_name) as dynamodb:
            table = await dynamodb.Table(self.table_name)
            yield table

    async def find_user_by_tax_id(self, tax_id: str):
        async with self.get_table() as table:
            response = await table.query(
                IndexName='TaxIDIndex',  # nome do GSI
                KeyConditionExpression=Key('tax_id').eq(tax_id)
            )
            items = response.get('Items', [])
            return items[0] if items else None

    async def create_user(self, user_data: dict):
        async with self.get_table() as table:
            await table.put_item(Item=user_data)