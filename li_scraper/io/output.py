from abc import ABC, abstractmethod

class ExportResults(ABC):
    @abstractmethod
    def put(self):
        pass


class DynamoDBExport(ExportResults):
    def __init__(
        self,
        table: str
        ):
        self.db = boto3.resource('dynamodb')
        self.table = db.Table(table)

    def put(data: list):
        with self.table.batch_writer() as batch:
            for data_point in data:
                batch.put_item(
                    Item=data_point
                    )
