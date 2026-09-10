# Project Instructions for GitHub Copilot

## Project

This project is a Flask-based Sudoku web application being refactored from legacy Python code.

## Technology Stack

- Backend: Python 3, Flask
- Frontend: HTML, CSS, vanilla JavaScript
- Testing: pytest
- Browser persistence: localStorage
- No frontend framework is required.

## Project Structure

- `starter/app.py` contains the Flask application and routes.
- `starter/sudoku_logic.py` contains Sudoku generation, solving and validation logic.
- `starter/templates/` contains HTML templates.
- `starter/static/` contains CSS and JavaScript.
- `starter/tests/` contains automated pytest tests.
- `Screenshots/` contains evidence of GitHub Copilot development.

## Coding Conventions

- Keep functions small and focused.
- Use descriptive names.
- Prefer modular, reusable functions.
- Avoid unnecessary duplication.
- Keep Sudoku logic separate from Flask route handling.
- Keep browser/UI logic separate from Python Sudoku logic.
- Add comments only when they explain non-obvious decisions.
- Preserve existing working behavior when refactoring.
- Do not rewrite the entire application when a targeted change is sufficient.
- Handle invalid input safely.
- Do not introduce global mutable state unless necessary.

## Sudoku Rules

The Sudoku board is 9x9 and contains nine 3x3 regions.

Every generated puzzle MUST have exactly one unique solution.

Use a reliable backtracking-based solver or equivalent deterministic solution-counting approach to validate uniqueness.

Difficulty levels:

- Easy: most prefilled cells
- Medium: fewer prefilled cells
- Hard: fewest prefilled cells

Prefilled cells must remain locked and must never be editable by the player.

Hint-filled cells must also become locked after the hint is applied.

## Validation Rules

The application must detect:

- Duplicate values in a row
- Duplicate values in a column
- Duplicate values in a 3x3 region
- Incorrect values compared with the puzzle solution
- Invalid user entries

Invalid/conflicting cells should receive immediate visual feedback.

The Check feature must identify incorrect entries without modifying correct entries.

The puzzle is complete only when every cell contains the correct value.

## Game Features

The application must support:

- New Game
- Easy/Medium/Hard difficulty
- Hint
- Check
- Conflict highlighting
- Timer
- Player name
- Top 10 leaderboard
- Difficulty recorded with scores
- Hint count recorded with scores
- localStorage persistence
- Dark mode
- Light mode
- Responsive mobile and desktop layout
- Alternating visual treatment for the nine 3x3 Sudoku regions

## Timer

- Start when a new game begins.
- Reset when a new game begins.
- Stop when the puzzle is correctly completed.
- Do not continue counting after completion.

## Leaderboard

Store completed-game scores using browser localStorage.

Each score should contain:

- Player name
- Completion time
- Difficulty
- Number of hints

Keep only the best 10 scores.

Lower completion time is better.

Only successfully completed games should be recorded.

Corrupted localStorage data must not crash the application.

## UI Requirements

The application must work on:

- Desktop
- Tablet
- Mobile

Avoid horizontal overflow.

Buttons and inputs must remain usable on small screens.

Text and controls must remain readable in both light and dark modes.

Sudoku 3x3 regions must remain visually distinguishable.

Validation/conflict highlighting must remain visible in both themes.

## Testing Requirements

Use pytest for backend/core logic.

Do not delete tests merely to make the test suite pass.

Tests should cover:

- Sudoku generation
- Unique solution validation
- Difficulty levels
- Locked cells
- Conflict detection
- Check behavior
- Hint behavior
- Hint locking
- Timer behavior where practical
- Leaderboard behavior
- Score sorting
- Top 10 limit
- localStorage-related behavior where practical

Run the complete test suite after significant changes:

`python -m pytest`

## GitHub Copilot Usage

Before making significant changes:

1. Inspect the existing implementation.
2. Explain the proposed approach.
3. Identify affected files.
4. Make the smallest reasonable change.
5. Review the generated code before accepting it.
6. Run tests after the change.
7. Fix failures rather than removing tests.

Do not blindly accept Copilot suggestions.

If a Copilot suggestion conflicts with these instructions or introduces unnecessary complexity, reject or modify the suggestion and document the reasoning.

## Important Constraints

Do NOT:

- Replace the entire application unnecessarily.
- Remove existing functionality.
- Remove tests simply because they fail.
- Use hard-coded puzzle solutions as a substitute for solving.
- Treat a puzzle as valid without checking uniqueness.
- Make prefilled or hinted cells editable.
- Store leaderboard data only in Python memory.
- break mobile layouts while improving desktop styling.
