from export.base import ExportResults

import boto3


class DynamoDBExport(ExportResults):
    def __init__(
        self,
        table: str
        ):
        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(table)

    def put(self, data: list):
        with self.table.batch_writer() as batch:
            for data_point in data:
                batch.put_item(
                    Item=data_point
                    )
