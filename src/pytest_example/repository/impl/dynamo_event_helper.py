from typing import Optional

import aioboto3
from fastapi import FastAPI

from pytest_example.repository.impl.dynamo_db_todo import DynamoDbTODOStore


def dynamo_start_up(app: FastAPI, endpoint_url: Optional[str] = None):
    @app.on_event("startup")
    async def bootstrap_dynamo():
        session = aioboto3.Session()
        async with session.resource(
            "dynamodb", region_name="us-east-1", endpoint_url=endpoint_url
        ) as dynamo_resource:
            await DynamoDbTODOStore.initialize_table_schema(dynamo_resource)

    return bootstrap_dynamo
