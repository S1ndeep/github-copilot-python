import copy

import pytest

import sudoku_logic
from app import CURRENT, app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    CURRENT['puzzle'] = None
    CURRENT['solution'] = None
    with app.test_client() as test_client:
        yield test_client
    CURRENT['puzzle'] = None
    CURRENT['solution'] = None


def test_generate_puzzle_returns_a_valid_board_and_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert all(len(row) == sudoku_logic.SIZE for row in solution)
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35
    assert all(
        sorted(row) == list(range(1, sudoku_logic.SIZE + 1))
        for row in solution
    )
    assert all(
        sorted(solution[row][column] for row in range(sudoku_logic.SIZE))
        == list(range(1, sudoku_logic.SIZE + 1))
        for column in range(sudoku_logic.SIZE)
    )


def test_index_renders_the_game_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data
    assert b'id="sudoku-board"' in response.data


def test_new_game_returns_a_puzzle_and_stores_its_solution(client):
    response = client.get('/new?clues=40')

    assert response.status_code == 200
    puzzle = response.get_json()['puzzle']
    assert puzzle == CURRENT['puzzle']
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 40
    assert CURRENT['solution'] is not None


def test_check_returns_an_error_when_no_game_is_in_progress(client):
    response = client.post('/check', json={'board': sudoku_logic.create_empty_board()})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_accepts_the_stored_solution(client):
    client.get('/new')

    response = client.post('/check', json={'board': copy.deepcopy(CURRENT['solution'])})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_check_reports_incorrect_cells(client):
    client.get('/new')
    board = copy.deepcopy(CURRENT['solution'])
    board[0][0] = sudoku_logic.EMPTY

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert [0, 0] in response.get_json()['incorrect']