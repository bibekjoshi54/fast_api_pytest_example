import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock, AsyncMock

from pytest_example.entity.todo import TODOEntity
from pytest_example.repository.interface.itodo_repo import ITodoRepo
from pytest_example.usecase.create_todo import CreateToDoUsecase


class TestCreateTODO:

    @pytest.mark.asyncio
    async def test_orchestrate(self, mocker: MockerFixture):
        self._mocker = mocker
        await self.perform_creation()

    def _mock_itodo_repo(self):
        return Mock(spec=ITodoRepo)

    async def perform_creation(self):
        repo = self._mock_itodo_repo()

        todo = TODOEntity(name="dummy", description="dummy")

        self._mocker.patch.object(
            target=repo,
            attribute="create_todo",
            side_effect=AsyncMock(return_value=todo),
        )

        usecase = CreateToDoUsecase(repo)
        result = await usecase.execute('dummy', 'dummy')
        assert todo == result

        repo.create_todo.assert_called_once()

