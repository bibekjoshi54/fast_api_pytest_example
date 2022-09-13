import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock, AsyncMock

from pytest_example.entity.todo import TODOEntity, TODOStatusEnum
from pytest_example.repository.interface.itodo_repo import ITodoRepo
from pytest_example.usecase.mark_complete_todo import MarkTodoCompleteUsecase


class TestMarkTodoCompleteUsecase:

    @pytest.mark.asyncio
    async def test_orchestrate(self, mocker: MockerFixture):
        self._mocker = mocker
        await self.perform_successfull_execute()
        await self.perform_unsuccessfull_execute()

    def _mock_itodo_repo(self):
        return Mock(spec=ITodoRepo)

    async def perform_successfull_execute(self):
        repo = self._mock_itodo_repo()

        todo = TODOEntity(name="dummy-1", description="dummy-1")
        new_todo_completed = TODOEntity(**dict(todo))
        new_todo_completed.change_transition(TODOStatusEnum.COMPLETED)

        self._mocker.patch.object(
            target=repo,
            attribute="read_todo",
            side_effect=AsyncMock(return_value=todo),
        )

        self._mocker.patch.object(
            target=repo,
            attribute="update_todo",
            side_effect=AsyncMock(return_value=new_todo_completed),
        )

        usecase = MarkTodoCompleteUsecase(repo)
        result = await usecase.execute(todo.id)
        assert todo == result

        repo.update_todo.assert_called_with(new_todo_completed)

    async def perform_unsuccessfull_execute(self):
        repo = self._mock_itodo_repo()

        todo = TODOEntity(name="dummy-1", description="dummy-1")
        todo.change_transition(TODOStatusEnum.COMPLETED)

        self._mocker.patch.object(
            target=repo,
            attribute="read_todo",
            side_effect=ValueError(),
        )

        usecase = MarkTodoCompleteUsecase(repo)

        with pytest.raises(ValueError) as e_info:
            await usecase.execute(todo.id)

        repo.read_todo.assert_called_once()

        self._mocker.patch.object(
            target=repo,
            attribute="read_todo",
            side_effect=AsyncMock(return_value=todo),
        )

        usecase = MarkTodoCompleteUsecase(repo)

        with pytest.raises(ValueError) as e_info:
            await usecase.execute(todo.id)





