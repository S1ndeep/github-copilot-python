from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
    'locked': [],
    'hints_used': 0,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty')
    if difficulty is not None:
        try:
            puzzle, solution = sudoku_logic.generate_puzzle_for_difficulty(difficulty)
        except ValueError as error:
            return jsonify({'error': str(error)}), 400
    else:
        clues = int(request.args.get('clues', 35))
        puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['locked'] = sudoku_logic.get_locked_cells(puzzle)
    CURRENT['hints_used'] = 0
    return jsonify({'puzzle': puzzle, 'locked': CURRENT['locked'], 'hints_used': 0})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    locked = [
        [row, col]
        for row, col in CURRENT['locked']
        if board[row][col] != (puzzle[row][col] or solution[row][col])
    ]
    if locked:
        return jsonify({'error': 'Locked cells cannot be changed', 'locked': locked}), 400
    conflicts = sudoku_logic.find_conflicts(board)
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({
        'incorrect': incorrect,
        'conflicts': conflicts,
        'solved': not incorrect and not conflicts,
    })


@app.route('/hint', methods=['POST'])
def get_hint():
    data = request.json or {}
    board = data.get('board')
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    if not isinstance(board, list) or len(board) != sudoku_logic.SIZE:
        return jsonify({'error': 'Invalid board'}), 400

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if [row, col] in CURRENT['locked']:
                continue
            if board[row][col] != solution[row][col]:
                CURRENT['locked'].append([row, col])
                CURRENT['hints_used'] += 1
                return jsonify({
                    'row': row,
                    'col': col,
                    'value': solution[row][col],
                    'locked': CURRENT['locked'],
                    'hints_used': CURRENT['hints_used'],
                })
    return jsonify({'error': 'No unsolved cells available', 'hints_used': CURRENT['hints_used']}), 400

if __name__ == '__main__':
    app.run(debug=True)