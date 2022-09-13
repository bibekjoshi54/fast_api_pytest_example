import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock, AsyncMock

from pytest_example.entity.todo import TODOEntity
from pytest_example.repository.interface.itodo_repo import ITodoRepo
from pytest_example.usecase.list_todo import ListToDoUsecase


class TestListTODO:

    @pytest.mark.asyncio
    async def test_orchestrate(self, mocker: MockerFixture):
        self._mocker = mocker
        await self.perform_list()

    def _mock_itodo_repo(self):
        return Mock(spec=ITodoRepo)

    async def perform_list(self):
        repo = self._mock_itodo_repo()

        todo = [TODOEntity(name="dummy-1", description="dummy-1"), TODOEntity(name="dummy-2", description="dummy-2")]

        self._mocker.patch.object(
            target=repo,
            attribute="list_todo",
            side_effect=AsyncMock(return_value=todo),
        )

        usecase = ListToDoUsecase(repo)
        result = await usecase.execute()
        assert todo == result

        repo.list_todo.assert_called_once()

