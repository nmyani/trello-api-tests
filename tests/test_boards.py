import pytest
from utils.trello_client import create_board, get_board, update_board, delete_board


class TestBoardCreate:
    def test_create_board_returns_200(self):
        response = create_board("Test Board - Create")
        assert response.status_code == 200
        delete_board(response.json()["id"])

    def test_create_board_response_contains_name(self):
        name = "Test Board - Name Check"
        response = create_board(name)
        assert response.json()["name"] == name
        delete_board(response.json()["id"])

    def test_create_board_response_contains_id(self):
        response = create_board("Test Board - ID Check")
        assert "id" in response.json()
        delete_board(response.json()["id"])

    @pytest.mark.parametrize("name", [
        "Board Alpha",
        "Board with numbers 123",
        "Board-with-hyphens",
    ])
    def test_create_board_various_names(self, name):
        response = create_board(name)
        assert response.status_code == 200
        assert response.json()["name"] == name
        delete_board(response.json()["id"])


class TestBoardRead:
    def test_get_board_returns_200(self, board):
        response = get_board(board["id"])
        assert response.status_code == 200

    def test_get_board_id_matches(self, board):
        response = get_board(board["id"])
        assert response.json()["id"] == board["id"]

    def test_get_board_nonexistent_id_returns_404(self):
        """Valid format ID that does not exist on Trello returns 404."""
        valid_format_nonexistent_id = "aaaaaaaaaaaaaaaaaaaaaaaa"  # 24 hex chars
        response = get_board(valid_format_nonexistent_id)
        assert response.status_code == 404

    def test_get_board_invalid_format_id_returns_400(self):
        """ID that does not match ^[0-9a-fA-F]{24}$ returns 400 Bad Request."""
        response = get_board("invalid-id-format")
        assert response.status_code == 400
        assert response.text == "invalid id"


class TestBoardUpdate:
    def test_update_board_name(self, board):
        response = update_board(board["id"], name="Updated Board Name")
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Board Name"

    def test_update_board_description(self, board):
        response = update_board(board["id"], desc="Automated test description")
        assert response.status_code == 200
        assert response.json()["desc"] == "Automated test description"


class TestBoardDelete:
    def test_delete_board_returns_200(self):
        board = create_board("Board to Delete")
        board_id = board.json()["id"]
        response = delete_board(board_id)
        assert response.status_code == 200

    def test_get_deleted_board_returns_404(self):
        board = create_board("Board to Delete and Verify")
        board_id = board.json()["id"]
        delete_board(board_id)
        response = get_board(board_id)
        assert response.status_code == 404
