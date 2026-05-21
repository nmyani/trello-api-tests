import pytest
from utils.trello_client import create_list, get_list, update_list, archive_list


class TestListCreate:
    def test_create_list_returns_200(self, board):
        response = create_list(board["id"], "New List")
        assert response.status_code == 200

    def test_create_list_response_contains_name(self, board):
        name = "Named List"
        response = create_list(board["id"], name)
        assert response.json()["name"] == name

    def test_create_list_linked_to_correct_board(self, board):
        response = create_list(board["id"], "Board-Linked List")
        assert response.json()["idBoard"] == board["id"]

    @pytest.mark.parametrize("name", [
        "To Do",
        "In Progress",
        "Done",
    ])
    def test_create_standard_kanban_lists(self, board, name):
        response = create_list(board["id"], name)
        assert response.status_code == 200
        assert response.json()["name"] == name


class TestListRead:
    def test_get_list_returns_200(self, trello_list):
        response = get_list(trello_list["id"])
        assert response.status_code == 200

    def test_get_list_id_matches(self, trello_list):
        response = get_list(trello_list["id"])
        assert response.json()["id"] == trello_list["id"]

    def test_get_list_nonexistent_id_returns_404(self):
        """Valid format ID that does not exist in Trello returns 404."""
        valid_format_nonexistent_id = "aaaaaaaaaaaaaaaaaaaaaaaa"  # 24 hex chars
        response = get_list(valid_format_nonexistent_id)
        assert response.status_code == 404

    def test_get_list_invalid_format_id_returns_400(self):
        """ID that does not match ^[0-9a-fA-F]{24}$ returns 400 Bad Request."""
        response = get_list("invalid-id-format")
        assert response.status_code == 400
        assert response.text == "invalid id"

class TestListUpdate:
    def test_update_list_name(self, trello_list):
        response = update_list(trello_list["id"], name="Renamed List")
        assert response.status_code == 200
        assert response.json()["name"] == "Renamed List"


class TestListArchive:
    def test_archive_list_returns_200(self, trello_list):
        response = archive_list(trello_list["id"])
        assert response.status_code == 200

    def test_archived_list_is_closed(self, trello_list):
        archive_list(trello_list["id"])
        response = get_list(trello_list["id"])
        assert response.json()["closed"] is True
