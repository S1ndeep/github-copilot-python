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
    assert sudoku_logic.count_solutions(puzzle) == 1


def test_solver_finds_the_unique_solution_for_a_known_puzzle():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    solution = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    assert sudoku_logic.count_solutions(puzzle) == 1
    assert sudoku_logic.solve_board(puzzle) == solution


def test_solver_stops_after_finding_multiple_solutions():
    puzzle = sudoku_logic.create_empty_board()

    assert sudoku_logic.count_solutions(puzzle) == 2


def test_solver_returns_no_solution_for_invalid_or_unsolvable_boards():
    invalid_board = sudoku_logic.create_empty_board()
    invalid_board[0][0] = 1
    invalid_board[0][1] = 1
    unsolvable_board = sudoku_logic.create_empty_board()
    unsolvable_board[0] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    unsolvable_board[1][0] = 1

    assert sudoku_logic.count_solutions(invalid_board) == 0
    assert sudoku_logic.solve_board(invalid_board) is None
    assert sudoku_logic.count_solutions(unsolvable_board) == 0
    assert sudoku_logic.solve_board(unsolvable_board) is None


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