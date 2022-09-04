from pytest_example.entity.todo import TODOEntity
from pytest_example.repository.interface.itodo_repo import ITodoRepo


class ListToDoUsecase:
    def __init__(self, repo: ITodoRepo):

        self.repo = repo

    async def execute(
        self,
    ) -> list[TODOEntity]:
        return await self.repo.list_todo()
