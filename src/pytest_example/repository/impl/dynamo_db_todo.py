import botocore
from boto3.dynamodb.conditions import Key
from pydantic import parse_obj_as
from pytest_example.repository.interface.itodo_repo import ITodoRepo, TODOEntity


class DynamoDbTODOStore(ITodoRepo):
    TABLE_NAME = "TODO"

    @staticmethod
    def table_definition():
        """
        Ideally this shouldn't be declared like this.

        Returns: Table defination for the example

        """
        return {
            "TableName": DynamoDbTODOStore.TABLE_NAME,
            "KeySchema": [{"AttributeName": "id", "KeyType": "HASH"}],
            "AttributeDefinitions": [{"AttributeName": "id", "AttributeType": "S"}],
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 100,
                "WriteCapacityUnits": 100,
            },
        }

    @staticmethod
    async def initialize_table_schema(dynamodb):
        try:
            table = await dynamodb.create_table(**DynamoDbTODOStore.table_definition())
            return table

        except botocore.exceptions.ClientError as error:
            if error.response["Error"]["Code"] == "ResourceInUseException":
                print("Database already exists")
            else:
                raise error

    def __init__(self, dynamo_table_client):
        self._dynamo_table_client = dynamo_table_client

    async def create_todo(self, todo: TODOEntity) -> TODOEntity:
        await self._dynamo_table_client.put_item(Item={**dict(todo)})
        return todo

    async def read_todo(self, todo_id: str) -> TODOEntity:
        todo_json = await self._dynamo_table_client.query(
            KeyConditionExpression=Key("id").eq(todo_id)
        )

        try:
            return TODOEntity.parse_obj(todo_json["Items"][0])
        except IndexError:
            raise ValueError(f"The item with id {todo_id} doesn't exist")

    async def update_todo(self, todo: TODOEntity) -> TODOEntity:
        return await self.create_todo(todo)

    async def list_todo(self) -> list[TODOEntity]:
        todos = await self._dynamo_table_client.scan()
        return parse_obj_as(list[TODOEntity], todos["Items"])

    #
    # if __name__ == '__main__':
    #     import aioboto3
    #     import asyncio
    #     from pprint import pprint as print
    #
    async def main():
        session = aioboto3.Session()
        async with session.resource(
            "dynamodb", region_name="us-east-1", endpoint_url="http://localhost:4566"
        ) as dynamo_resource:
            create_table = await DynamoDbTODOStore.initialize_table_schema(
                dynamo_resource
            )
            table = await dynamo_resource.Table(DynamoDbTODOStore.TABLE_NAME)
            repo = DynamoDbTODOStore(dynamo_table_client=table)
            todo = TODOEntity(
                name="TESTDYNAMO---UPDATE-2", description="Testing the dynamo"
            )
            await repo.create_todo(todo)
            todo = await repo.read_todo("3e3b77a795bd4a5d949a2f911b3c8866")
            print(todo)
            print(await repo.list_todo())


#
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
