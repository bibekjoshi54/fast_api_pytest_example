from starlette.testclient import TestClient

MOCK_DATA = {"task_name": "name-of-task", "task_description": "sample-description"}


class TestTODOResource:
    def test_orchestrator(self, rest_client: TestClient):
        self.empty_get(rest_client)
        self.insert_data_id = self.insert_todo(rest_client)
        self.get_all_todo(rest_client)
        self.mark_as_complete_todo(rest_client)
        self.invalid_mark_as_complete_todo(rest_client)

    def empty_get(self, rest_client: TestClient):
        response = rest_client.get("/api/todo/")
        assert response.status_code == 200
        assert response.json() == []

    def insert_todo(self, rest_client: TestClient):
        post_data_mock = MOCK_DATA
        response = rest_client.post("/api/todo/", json=post_data_mock)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["name"] == post_data_mock["task_name"]
        assert response_data["description"] == post_data_mock["task_description"]
        assert response_data["id"] is not None
        assert response_data["status"] == "PENDING"
        return response_data["id"]

    def get_all_todo(self, rest_client: TestClient):
        response_assert_data = [
            {
                "id": self.insert_data_id,
                "name": MOCK_DATA["task_name"],
                "description": MOCK_DATA["task_description"],
                "status": "PENDING",
            }
        ]
        response = rest_client.get("/api/todo/")
        assert response.status_code == 200
        response_data = response.json()
        assert response_assert_data == response_data

    def mark_as_complete_todo(self, rest_client: TestClient):
        response_assert_data = {
            "id": self.insert_data_id,
            "name": MOCK_DATA["task_name"],
            "description": MOCK_DATA["task_description"],
            "status": "COMPLETED",
        }

        response = rest_client.post(
            "/api/todo/mark-as-completed", params={"todo_id": self.insert_data_id}
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_assert_data == response_data

    def invalid_mark_as_complete_todo(self, rest_client: TestClient):
        response = rest_client.post(
            "/api/todo/mark-as-completed", params={"todo_id": self.insert_data_id}
        )
        assert response.status_code == 418
