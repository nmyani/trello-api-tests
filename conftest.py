import pytest
from utils.trello_client import create_board, delete_board, create_list, create_card, delete_card


# ── Session-level board: shared across all tests ───────────────────────────────

@pytest.fixture(scope="session")
def board():
    """Create a test board once per session, delete it after all tests."""
    response = create_board("QA Test Board — Automated")
    assert response.status_code == 200, f"Board creation failed: {response.text}"
    board_data = response.json()
    yield board_data
    delete_board(board_data["id"])


# ── Function-level list: fresh list per test that needs it ────────────────────

@pytest.fixture
def trello_list(board):
    """Create a list on the shared board for each test."""
    response = create_list(board["id"], "Test List")
    assert response.status_code == 200, f"List creation failed: {response.text}"
    yield response.json()


# ── Function-level card: fresh card per test that needs it ────────────────────

@pytest.fixture
def trello_card(trello_list):
    """Create a card in the test list, delete it after the test."""
    response = create_card(trello_list["id"], "Test Card", desc="Created by pytest")
    assert response.status_code == 200, f"Card creation failed: {response.text}"
    card_data = response.json()
    yield card_data
    delete_card(card_data["id"])
