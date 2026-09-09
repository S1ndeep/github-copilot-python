# Sudoku Game

A Flask-backed Sudoku game with generated puzzles, server-side solution checking, hints, a timer, a persistent local leaderboard, and a responsive browser UI.

## Features

- Easy, Medium, and Hard difficulty levels.
- Puzzle generation with unique-solution validation.
- Locked prefilled cells that cannot be edited.
- Check Solution button for comparing entries with the solution.
- Hint button that fills and locks a correct cell.
- Conflict feedback for duplicate values in rows, columns, and 3x3 regions.
- Incorrect-entry feedback for values that do not match the solution.
- Timer that starts with a new game and stops after successful completion.
- Player name input for completed scores.
- Top 10 leaderboard sorted by completion time.
- Scores include player name, completion time, difficulty, and hint count.
- Leaderboard persistence through browser `localStorage`.
- Dark/light mode toggle with saved theme preference.
- Responsive desktop, tablet, and mobile layout.
- Alternating visual treatment for the nine 3x3 Sudoku regions.

## Project Structure

```text
.
├── pytest.ini
├── README.md
└── starter/
	├── app.py
	├── requirements.txt
	├── sudoku_logic.py
	├── static/
	│   ├── leaderboard.js
	│   ├── main.js
	│   └── styles.css
	├── templates/
	│   └── index.html
	└── tests/
		├── leaderboard.test.js
		└── test_legacy_behavior.py
```

`starter/app.py` is the Flask entry point. `starter/sudoku_logic.py` contains board validation, puzzle generation, solving, and conflict detection. The browser interface is defined by `starter/templates/index.html` and the files in `starter/static/`.

## Requirements

- Python 3.8 or newer.
- A modern web browser with JavaScript and `localStorage` support.
- Python packages listed in `starter/requirements.txt`: Flask and pytest.
- Node.js is optional and is only required for the standalone leaderboard tests.

## Setup and Installation

From the repository root, create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux, use:

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r starter/requirements.txt
```

## Run the Application

From the repository root, run:

```bash
python starter/app.py
```

Then open <http://127.0.0.1:5000> in a browser.

## How to Play

1. Select Easy, Medium, or Hard.
2. Click **New Game**. A new puzzle starts the timer and resets the hint count.
3. Enter digits from 1 through 9 in the editable cells. Prefilled and hinted cells are locked.
4. Click **Check Solution** to see incorrect entries and Sudoku conflicts.
5. Correct highlighted cells or click **Hint** to fill and lock one correct unsolved cell.
6. Complete every cell correctly and click **Check Solution**. The timer stops and the completed game can be added to the leaderboard.

## Leaderboard

Only successfully completed games are recorded. The player name, elapsed time, selected difficulty, and number of hints used are stored as a score. Scores are sorted from the lowest completion time to the highest, and only the ten best scores are retained.

Scores are stored in browser `localStorage` under the key `sudoku.top10Scores.v1`. Invalid or corrupted stored data is ignored so it does not prevent the game from loading. Repeated checks after completing the same puzzle do not add duplicate scores.

## Dark and Light Mode

Use the **Dark mode** or **Light mode** button in the page header. The selected theme is stored in browser `localStorage` under `sudoku.theme.v1` and is restored when the application is reopened. Switching themes does not start a new game or reset the current timer.

## Testing

Run the complete Python test suite from the repository root:

```bash
python -m pytest
```

The suite covers the Flask routes, puzzle generation and unique solutions, difficulty levels, locked cells, hints, solution checking, and conflict detection.

The isolated browser leaderboard module also has optional dependency-free Node.js tests:

```bash
node --test starter/tests/leaderboard.test.js
```

The Node tests cover leaderboard sorting, the Top 10 limit, score metadata, persistence, and corrupted `localStorage` data.

## Copilot Development Instructions

No `instruction.md` file is currently present in this repository. The original project guidance is retained in the repository history and the current implementation is documented here. `pytest.ini` contains the test import-path configuration that allows the exact command `python -m pytest` to run from the repository root.
