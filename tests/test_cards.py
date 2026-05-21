import pytest
from utils.trello_client import create_card, get_card, update_card, delete_card


class TestCardCreate:
    def test_create_card_returns_200(self, trello_list):
        response = create_card(trello_list["id"], "New Card")
        assert response.status_code == 200
        delete_card(response.json()["id"])

    def test_create_card_name_matches(self, trello_list):
        name = "Specific Card Name"
        response = create_card(trello_list["id"], name)
        assert response.json()["name"] == name
        delete_card(response.json()["id"])

    def test_create_card_with_description(self, trello_list):
        desc = "This is a test description"
        response = create_card(trello_list["id"], "Card with Desc", desc=desc)
        assert response.json()["desc"] == desc
        delete_card(response.json()["id"])

    def test_create_card_linked_to_correct_list(self, trello_list):
        response = create_card(trello_list["id"], "List-Linked Card")
        assert response.json()["idList"] == trello_list["id"]
        delete_card(response.json()["id"])

    @pytest.mark.parametrize("name,desc", [
        ("Bug Report", "Steps to reproduce the issue"),
        ("Feature Request", "User story description"),
        ("Tech Debt", "Refactoring needed"),
    ])
    def test_create_various_card_types(self, trello_list, name, desc):
        response = create_card(trello_list["id"], name, desc=desc)
        assert response.status_code == 200
        assert response.json()["name"] == name
        assert response.json()["desc"] == desc
        delete_card(response.json()["id"])


class TestCardRead:
    def test_get_card_returns_200(self, trello_card):
        response = get_card(trello_card["id"])
        assert response.status_code == 200

    def test_get_card_id_matches(self, trello_card):
        response = get_card(trello_card["id"])
        assert response.json()["id"] == trello_card["id"]

    def test_get_card_nonexistent_id_returns_404(self):
        """Valid format ID that does not exist in Trello returns 404."""
        valid_format_nonexistent_id = "aaaaaaaaaaaaaaaaaaaaaaaa"  # 24 hex chars
        response = get_card(valid_format_nonexistent_id)
        assert response.status_code == 404

    def test_get_card_invalid_format_id_returns_400(self):
        """ID that does not match ^[0-9a-fA-F]{24}$ returns 400 Bad Request."""
        response = get_card("invalid-id-format")
        assert response.status_code == 400
        assert response.text == "invalid id"
        
    def test_get_card_contains_expected_fields(self, trello_card):
        response = get_card(trello_card["id"])
        data = response.json()
        for field in ["id", "name", "desc", "idList", "idBoard"]:
            assert field in data, f"Missing expected field: {field}"


class TestCardUpdate:
    def test_update_card_name(self, trello_card):
        response = update_card(trello_card["id"], name="Updated Card Name")
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Card Name"

    def test_update_card_description(self, trello_card):
        response = update_card(trello_card["id"], desc="Updated description")
        assert response.status_code == 200
        assert response.json()["desc"] == "Updated description"

    def test_update_card_set_due_date(self, trello_card):
        response = update_card(trello_card["id"], due="2025-12-31T12:00:00.000Z")
        assert response.status_code == 200
        assert response.json()["due"] is not None


class TestCardDelete:
    def test_delete_card_returns_200(self, trello_list):
        card = create_card(trello_list["id"], "Card to Delete")
        card_id = card.json()["id"]
        response = delete_card(card_id)
        assert response.status_code == 200

    def test_get_deleted_card_returns_404(self, trello_list):
        card = create_card(trello_list["id"], "Card to Delete and Verify")
        card_id = card.json()["id"]
        delete_card(card_id)
        response = get_card(card_id)
        assert response.status_code == 404
