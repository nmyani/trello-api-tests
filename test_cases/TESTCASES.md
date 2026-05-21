# Test Cases — Trello API Test Suite

This document describes all test cases covered by the automated test suite.  
Each test case maps directly to a test in the corresponding `tests/` file.

---

## Conventions

| Field | Description |
|---|---|
| **ID** | Unique identifier per entity and operation |
| **Test Name** | Matches the pytest function name |
| **Preconditions** | What must exist before the test runs |
| **Steps** | What the test does |
| **Expected Result** | What a passing test verifies |
| **Type** | Positive / Negative / Parametrized |

---

## 1. Boards

### 1.1 Create Board

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-B-01 | `test_create_board_returns_200` | Valid API credentials | Send POST /boards with a board name | Response status is 200 | Positive |
| TC-B-02 | `test_create_board_response_contains_name` | Valid API credentials | Send POST /boards with name "Test Board - Name Check" | Response body `name` matches the sent value | Positive |
| TC-B-03 | `test_create_board_response_contains_id` | Valid API credentials | Send POST /boards | Response body contains field `id` | Positive |
| TC-B-04 | `test_create_board_various_names` | Valid API credentials | Send POST /boards with names: "Board Alpha", "Board with numbers 123", "Board-with-hyphens" | Each response returns status 200 and `name` matches input | Parametrized |

### 1.2 Read Board

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-B-05 | `test_get_board_returns_200` | Session board exists | Send GET /boards/{id} with valid board ID | Response status is 200 | Positive |
| TC-B-06 | `test_get_board_id_matches` | Session board exists | Send GET /boards/{id} | Response body `id` matches the requested board ID | Positive |
| TC-B-07 | `test_get_board_nonexistent_id_returns_404` | — | Send GET /boards/{id} with valid-format ID that does not exist | Response status is 404 | Negative |
| TC-B-08 | `test_get_board_invalid_format_id_returns_400` | — | Send GET /boards/{id} with invalid ID format (not matching ^[0-9a-fA-F]{24}$) | Response status is 400 | Negative |

### 1.3 Update Board

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-B-09 | `test_update_board_name` | Session board exists | Send PUT /boards/{id} with new name | Response status 200 and `name` reflects updated value | Positive |
| TC-B-10 | `test_update_board_description` | Session board exists | Send PUT /boards/{id} with new description | Response status 200 and `desc` reflects updated value | Positive |

### 1.4 Delete Board

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-B-11 | `test_delete_board_returns_200` | A board is created for this test | Send DELETE /boards/{id} | Response status is 200 | Positive |
| TC-B-12 | `test_get_deleted_board_returns_404` | A board is created and deleted | Send GET /boards/{id} after deletion | Response status is 404 | Negative |

---

## 2. Lists

### 2.1 Create List

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-L-01 | `test_create_list_returns_200` | Session board exists | Send POST /lists with board ID and list name | Response status is 200 | Positive |
| TC-L-02 | `test_create_list_response_contains_name` | Session board exists | Send POST /lists with name "Named List" | Response body `name` matches the sent value | Positive |
| TC-L-03 | `test_create_list_linked_to_correct_board` | Session board exists | Send POST /lists | Response body `idBoard` matches the board ID | Positive |
| TC-L-04 | `test_create_standard_kanban_lists` | Session board exists | Send POST /lists with names: "To Do", "In Progress", "Done" | Each response returns status 200 and `name` matches input | Parametrized |

### 2.2 Read List

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-L-05 | `test_get_list_returns_200` | Function-scoped list exists | Send GET /lists/{id} | Response status is 200 | Positive |
| TC-L-06 | `test_get_list_id_matches` | Function-scoped list exists | Send GET /lists/{id} | Response body `id` matches the requested list ID | Positive |
| TC-L-07 | `test_get_list_nonexistent_id_returns_404` | — | Send GET /lists/{id} with valid-format ID that does not exist | Response status is 404 | Negative |
| TC-L-08 | `test_get_list_invalid_format_id_returns_400` | — | Send GET /lists/{id} with invalid ID format (not matching ^[0-9a-fA-F]{24}$) | Response status is 400 | Negative |

### 2.3 Update List

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-L-09 | `test_update_list_name` | Function-scoped list exists | Send PUT /lists/{id} with new name | Response status 200 and `name` reflects updated value | Positive |

### 2.4 Archive List

> **Note:** The Trello API does not support deleting lists. Archiving (`closed: true`) is the intended and documented approach.

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-L-10 | `test_archive_list_returns_200` | Function-scoped list exists | Send PUT /lists/{id}/closed with value true | Response status is 200 | Positive |
| TC-L-11 | `test_archived_list_is_closed` | Function-scoped list exists | Archive list, then GET /lists/{id} | Response body `closed` is `true` | Positive |

---

## 3. Cards

### 3.1 Create Card

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-C-01 | `test_create_card_returns_200` | Function-scoped list exists | Send POST /cards with list ID and card name | Response status is 200 | Positive |
| TC-C-02 | `test_create_card_name_matches` | Function-scoped list exists | Send POST /cards with name "Specific Card Name" | Response body `name` matches the sent value | Positive |
| TC-C-03 | `test_create_card_with_description` | Function-scoped list exists | Send POST /cards with `desc` field | Response body `desc` matches the sent value | Positive |
| TC-C-04 | `test_create_card_linked_to_correct_list` | Function-scoped list exists | Send POST /cards | Response body `idList` matches the list ID | Positive |
| TC-C-05 | `test_create_various_card_types` | Function-scoped list exists | Send POST /cards with 3 name/desc combinations | Each response returns 200 with matching `name` and `desc` | Parametrized |

### 3.2 Read Card

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-C-06 | `test_get_card_returns_200` | Function-scoped card exists | Send GET /cards/{id} | Response status is 200 | Positive |
| TC-C-07 | `test_get_card_id_matches` | Function-scoped card exists | Send GET /cards/{id} | Response body `id` matches the requested card ID | Positive |
| TC-C-08 | `test_get_card_nonexistent_id_returns_404` | — | Send GET /cards/{id} with valid-format ID that does not exist | Response status is 404 | Negative |
| TC-C-09 | `test_get_card_invalid_format_id_returns_400` | — | Send GET /cards/{id} with invalid ID format (not matching ^[0-9a-fA-F]{24}$) | Response status is 400 | Negative |
| TC-C-10 | `test_get_card_contains_expected_fields` | Function-scoped card exists | Send GET /cards/{id} | Response body contains all required fields: `id`, `name`, `desc`, `idList`, `idBoard` | Positive |

### 3.3 Update Card

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-C-11 | `test_update_card_name` | Function-scoped card exists | Send PUT /cards/{id} with new name | Response status 200 and `name` reflects updated value | Positive |
| TC-C-12 | `test_update_card_description` | Function-scoped card exists | Send PUT /cards/{id} with new description | Response status 200 and `desc` reflects updated value | Positive |
| TC-C-13 | `test_update_card_set_due_date` | Function-scoped card exists | Send PUT /cards/{id} with a due date | Response status 200 and `due` field is not null | Positive |

### 3.4 Delete Card

| ID | Test Name | Preconditions | Steps | Expected Result | Type |
|---|---|---|---|---|---|
| TC-C-14 | `test_delete_card_returns_200` | A card is created for this test | Send DELETE /cards/{id} | Response status is 200 | Positive |
| TC-C-15 | `test_get_deleted_card_returns_404` | A card is created and deleted | Send GET /cards/{id} after deletion | Response status is 404 | Negative |
