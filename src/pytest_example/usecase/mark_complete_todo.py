from pytest_example.entity.todo import TODOEntity, TODOStatusEnum
from pytest_example.repository.interface.itodo_repo import ITodoRepo


class MarkTodoCompleteUsecase:
    def __init__(self, repo: ITodoRepo):

        self.repo = repo

    async def execute(self, todo_id: str) -> TODOEntity:
        todo = await self.repo.read_todo(todo_id)
        todo.change_transition(TODOStatusEnum.COMPLETED)
        todo = await self.repo.update_todo(todo)
        return todo
