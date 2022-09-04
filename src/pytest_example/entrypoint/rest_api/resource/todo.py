import aioboto3

from pytest_example.config import CONFIG_AWS_ENDPOINT
from pytest_example.entity.todo import TODOEntity
from pytest_example.repository.impl.dynamo_db_todo import DynamoDbTODOStore
from pytest_example.usecase.create_todo import CreateToDoUsecase
from pytest_example.usecase.list_todo import ListToDoUsecase
from pytest_example.usecase.mark_complete_todo import MarkTodoCompleteUsecase
from .router import TODO_ROUTER
from .dto import TODOCreateDTO


@TODO_ROUTER.get("/", response_model=list[TODOEntity])
async def list_all_todo():
    session = aioboto3.Session()
    async with session.resource(
        "dynamodb", region_name="us-east-1", endpoint_url=CONFIG_AWS_ENDPOINT
    ) as dynamo_resource:
        table = await dynamo_resource.Table(DynamoDbTODOStore.TABLE_NAME)
        repo = DynamoDbTODOStore(dynamo_table_client=table)
        usecase = ListToDoUsecase(repo=repo)
        return await usecase.execute()


@TODO_ROUTER.post("/", response_model=TODOEntity)
async def list_all_todo(todo_request: TODOCreateDTO):
    session = aioboto3.Session()
    async with session.resource(
        "dynamodb", region_name="us-east-1", endpoint_url=CONFIG_AWS_ENDPOINT
    ) as dynamo_resource:
        table = await dynamo_resource.Table(DynamoDbTODOStore.TABLE_NAME)
        repo = DynamoDbTODOStore(dynamo_table_client=table)
        usecase = CreateToDoUsecase(repo=repo)
        return await usecase.execute(**dict(todo_request))


@TODO_ROUTER.post("/mark-as-completed", response_model=TODOEntity)
async def mark_to_as_completed(todo_id: str):
    session = aioboto3.Session()
    async with session.resource(
        "dynamodb", region_name="us-east-1", endpoint_url=CONFIG_AWS_ENDPOINT
    ) as dynamo_resource:
        table = await dynamo_resource.Table(DynamoDbTODOStore.TABLE_NAME)
        repo = DynamoDbTODOStore(dynamo_table_client=table)
        usecase = MarkTodoCompleteUsecase(repo=repo)
        return await usecase.execute(todo_id=todo_id)
