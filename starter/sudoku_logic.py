import copy
import random

SIZE = 9
EMPTY = 0
MAX_GENERATION_ATTEMPTS = 100

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def is_valid_board(board):
    if not isinstance(board, (list, tuple)) or len(board) != SIZE:
        return False

    for row in board:
        if not isinstance(row, (list, tuple)) or len(row) != SIZE:
            return False
        if any(type(value) is not int or value < EMPTY or value > SIZE for value in row):
            return False

    for index in range(SIZE):
        row_values = [value for value in board[index] if value != EMPTY]
        column_values = [board[row][index] for row in range(SIZE) if board[row][index] != EMPTY]
        if len(row_values) != len(set(row_values)):
            return False
        if len(column_values) != len(set(column_values)):
            return False

    for start_row in range(0, SIZE, 3):
        for start_col in range(0, SIZE, 3):
            box_values = [
                board[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)
                if board[row][col] != EMPTY
            ]
            if len(box_values) != len(set(box_values)):
                return False

    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def _find_empty_cell_with_fewest_candidates(board):
    best_cell = None
    best_candidates = None
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] != EMPTY:
                continue
            candidates = [
                candidate
                for candidate in range(1, SIZE + 1)
                if is_safe(board, row, col, candidate)
            ]
            if not candidates:
                return (row, col), []
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_cell = (row, col)
                best_candidates = candidates
    return best_cell, best_candidates


def _search_solutions(board, solutions, limit):
    if len(solutions) >= limit:
        return

    cell, candidates = _find_empty_cell_with_fewest_candidates(board)
    if cell is None:
        solutions.append(deep_copy(board))
        return
    if not candidates:
        return

    row, col = cell
    for candidate in candidates:
        board[row][col] = candidate
        _search_solutions(board, solutions, limit)
        board[row][col] = EMPTY
        if len(solutions) >= limit:
            return


def count_solutions(board, limit=2):
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError('limit must be a positive integer')
    if not is_valid_board(board):
        return 0

    solutions = []
    _search_solutions(deep_copy(board), solutions, limit)
    return len(solutions)


def solve_board(board):
    if not is_valid_board(board):
        return None

    solutions = []
    _search_solutions(deep_copy(board), solutions, 1)
    return solutions[0] if solutions else None

def remove_cells(board, clues):
    attempts = SIZE * SIZE - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1

def generate_puzzle(clues=35):
    if not isinstance(clues, int) or isinstance(clues, bool) or not 0 <= clues <= SIZE * SIZE:
        raise ValueError(f'clues must be between 0 and {SIZE * SIZE}')

    for _ in range(MAX_GENERATION_ATTEMPTS):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        remove_cells(board, clues)
        puzzle = deep_copy(board)
        if count_solutions(puzzle) == 1:
            return puzzle, solution

    raise RuntimeError('Unable to generate a puzzle with a unique solution')
