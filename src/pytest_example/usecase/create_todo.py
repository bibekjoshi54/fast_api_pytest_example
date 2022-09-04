from pytest_example.entity.todo import TODOEntity
from pytest_example.repository.interface.itodo_repo import ITodoRepo


class CreateToDoUsecase:
    def __init__(self, repo: ITodoRepo):

        self.repo = repo

    async def execute(self, task_name: str, task_description: str) -> TODOEntity:
        new_todo = TODOEntity(name=task_name, description=task_description)
        return await self.repo.create_todo(new_todo)
