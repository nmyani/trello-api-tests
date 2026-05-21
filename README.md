# Trello API Test Suite

### ![Trello Tests Status](https://github.com/nmyani/trello-api-tests/actions/workflows/run-tests.yml/badge.svg)

Automated API test suite for the Trello REST API, built with **Python** and **pytest**.

Covers full CRUD operations for Boards, Lists, and Cards — including parametrized test cases, session-scoped fixtures, and response schema validation.

---

## Project Structure

```
trello_api_tests/
├── conftest.py              # Session and function-level pytest fixtures
├── pytest.ini               # pytest configuration
├── requirements.txt         # Dependencies
├── .env.example             # Environment variable template
├── .gitignore
├── utils/
│   └── trello_client.py     # Trello API client — all request methods
└── tests/
    ├── test_boards.py       # Board CRUD tests
    ├── test_lists.py        # List CRUD tests
    └── test_cards.py        # Card CRUD tests
```

---

## Test Coverage

| Entity | Create | Read | Update | Delete / Archive |
|--------|--------|------|--------|-----------------|
| Board  |  &#10004;     |  &#10004;   |  &#10004;     |        &#10004;       |
| List   |  &#10004;     |  &#10004;   |  &#10004;     |  &#10004; (archive)   |
| Card   |  &#10004;     |  &#10004;   |  &#10004;     |       &#10004;        |

**Test techniques used:**
- `pytest` fixtures with `scope="session"` and `scope="function"`
- `conftest.py` for shared setup and teardown
- `@pytest.mark.parametrize` for data-driven test cases
- HTTP status code validation
- Response body / schema field validation
- Negative testing (invalid IDs → 404)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/nmyani/trello-api-tests.git
cd trello-api-tests
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure credentials

Get your Trello API key and token from: https://trello.com/app-key

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```
TRELLO_API_KEY=your_api_key_here
TRELLO_TOKEN=your_token_here
```

> ***The `.env` file is listed in `.gitignore` and will never be committed.***

---

## Running the Tests

Run all tests:

```bash
pytest
```

Run a specific file:

```bash
pytest tests/test_boards.py
pytest tests/test_cards.py
```

Run with HTML report:

```bash
pytest --html=reports/report.html
```

---

## Key Design Decisions

- **Session-scoped board fixture** — one board is created per test session and deleted at the end, reducing API calls and cleanup overhead.
- **Function-scoped list and card fixtures** — each test gets a fresh list/card to ensure test isolation.
- **Trello API note:** Lists cannot be deleted via the API — archiving (`closed: true`) is the correct and intended approach, as per Trello API documentation.
- **Credentials** are loaded from `.env` via `python-dotenv` and never hardcoded.

---

## Tech Stack

- Python 3.10+
- pytest 8.x
- requests
- python-dotenv
- pytest-html (optional reporting)

