from abc import abstractmethod, ABC

from pytest_example.entity.todo import TODOEntity


class ITodoRepo(ABC):
    async def create_todo(self, todo: TODOEntity) -> TODOEntity:
        pass

    async def read_todo(self, todo_id: str) -> TODOEntity:
        pass

    async def update_todo(self, todo: TODOEntity) -> TODOEntity:
        pass

    async def list_todo(self) -> list[TODOEntity]:
        pass
