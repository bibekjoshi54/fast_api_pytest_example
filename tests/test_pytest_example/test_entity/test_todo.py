import pytest
from moto import mock_dynamodb

from pytest_example.entity.todo import TODOEntity, TODOStatusEnum

DEFAULT_ASSIGNMENT = {"name": "TEST-TODO", "description": "TEST-DESCRIPTION"}
PARAMETER_ASSIGNMENT = {
    **DEFAULT_ASSIGNMENT,
    "id": "test-id",
    "status": TODOStatusEnum.COMPLETED,
}


class TestTodo:
    def test_orchestrator(self):
        self.entity_default_assignment()
        self.entity_all_argument_assignment()
        self.invalid_staus_transition()

    def entity_default_assignment(self):
        default_parameter_assignment_mock = DEFAULT_ASSIGNMENT
        todo = TODOEntity.parse_obj(default_parameter_assignment_mock)
        assert todo.name == default_parameter_assignment_mock["name"]
        assert todo.description == default_parameter_assignment_mock["description"]
        assert todo.status == TODOStatusEnum.PENDING

    def entity_all_argument_assignment(self):
        mock_data = PARAMETER_ASSIGNMENT
        todo = TODOEntity.parse_obj(mock_data)
        assert todo.name == mock_data["name"]
        assert todo.description == mock_data["description"]
        assert todo.status == mock_data["status"]
        assert todo.id == mock_data["id"]

    def invalid_staus_transition(self):
        mock_data = PARAMETER_ASSIGNMENT
        todo = TODOEntity.parse_obj(mock_data)
        with pytest.raises(ValueError) as exc_info:
            todo.change_transition(TODOStatusEnum.COMPLETED)
