from mypy_boto3_dynamodb import ServiceResource

from boto3.dynamodb.conditions import Key

class DatabaseRepository:
    def __init__(self, resource: ServiceResource, table_name: str):
        self.table = resource.Table(table_name)

    def find_user_by_tax_id(self, tax_id: str) -> dict | None:
        response = self.table.query(
            IndexName="TaxIDIndex",
            KeyConditionExpression=Key('tax_id').eq(tax_id),
            Limit=1
        )
        if has_user := response.get('Items', None):
            return has_user[0]
        return None