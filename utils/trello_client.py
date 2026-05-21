import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.trello.com/1"


def get_auth_params() -> dict:
    """Return Trello authentication parameters loaded from .env"""
    return {
        "key": os.getenv("TRELLO_API_KEY"),
        "token": os.getenv("TRELLO_TOKEN"),
    }


def build_url(endpoint: str) -> str:
    return f"{BASE_URL}/{endpoint}"


# Boards

def create_board(name: str) -> requests.Response:
    return requests.post(
        build_url("boards"),
        params={**get_auth_params(), "name": name, "defaultLists": "false"},
    )


def get_board(board_id: str) -> requests.Response:
    return requests.get(
        build_url(f"boards/{board_id}"),
        params=get_auth_params(),
    )


def update_board(board_id: str, **kwargs) -> requests.Response:
    return requests.put(
        build_url(f"boards/{board_id}"),
        params={**get_auth_params(), **kwargs},
    )


def delete_board(board_id: str) -> requests.Response:
    return requests.delete(
        build_url(f"boards/{board_id}"),
        params=get_auth_params(),
    )


# Lists

def create_list(board_id: str, name: str) -> requests.Response:
    return requests.post(
        build_url("lists"),
        params={**get_auth_params(), "idBoard": board_id, "name": name},
    )


def get_list(list_id: str) -> requests.Response:
    return requests.get(
        build_url(f"lists/{list_id}"),
        params=get_auth_params(),
    )


def update_list(list_id: str, **kwargs) -> requests.Response:
    return requests.put(
        build_url(f"lists/{list_id}"),
        params={**get_auth_params(), **kwargs},
    )


def archive_list(list_id: str) -> requests.Response:
    """Lists cannot be deleted via API — archiving is the correct approach."""
    return requests.put(
        build_url(f"lists/{list_id}/closed"),
        params={**get_auth_params(), "value": "true"},
    )


# Cards

def create_card(list_id: str, name: str, desc: str = "") -> requests.Response:
    return requests.post(
        build_url("cards"),
        params={**get_auth_params(), "idList": list_id, "name": name, "desc": desc},
    )


def get_card(card_id: str) -> requests.Response:
    return requests.get(
        build_url(f"cards/{card_id}"),
        params=get_auth_params(),
    )


def update_card(card_id: str, **kwargs) -> requests.Response:
    return requests.put(
        build_url(f"cards/{card_id}"),
        params={**get_auth_params(), **kwargs},
    )


def delete_card(card_id: str) -> requests.Response:
    return requests.delete(
        build_url(f"cards/{card_id}"),
        params=get_auth_params(),
    )
