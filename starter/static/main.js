// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const THEME_STORAGE_KEY = 'sudoku.theme.v1';
let puzzle = [];
let lockedCells = new Set();
let hintsUsed = 0;
let timerInterval = null;
let timerStartedAt = 0;
let elapsedSeconds = 0;
let completionRecorded = false;

function applyTheme(theme) {
  const isDark = theme === 'dark';
  document.body.classList.toggle('dark-mode', isDark);
  const toggle = document.getElementById('theme-toggle');
  toggle.innerText = isDark ? 'Light mode' : 'Dark mode';
  toggle.setAttribute('aria-pressed', isDark.toString());
}

function loadTheme() {
  try {
    return localStorage.getItem(THEME_STORAGE_KEY) === 'dark' ? 'dark' : 'light';
  } catch (error) {
    return 'light';
  }
}

function toggleTheme() {
  const nextTheme = document.body.classList.contains('dark-mode') ? 'light' : 'dark';
  applyTheme(nextTheme);
  try {
    localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
  } catch (error) {
    // The game remains usable when browser storage is unavailable.
  }
}

function formatElapsedTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const seconds = Math.floor(totalSeconds % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

function updateTimer() {
  elapsedSeconds = Math.floor((Date.now() - timerStartedAt) / 1000);
  document.getElementById('timer').innerText = formatElapsedTime(elapsedSeconds);
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  timerStartedAt = Date.now();
  updateTimer();
  timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  if (timerStartedAt) updateTimer();
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz, lockedCellList) {
  puzzle = puz;
  lockedCells = new Set(lockedCellList.map(([row, col]) => row * SIZE + col));
  hintsUsed = 0;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const locked = lockedCells;
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (locked.has(idx)) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle, data.locked);
  completionRecorded = false;
  startTimer();
  document.getElementById('message').innerText = '';
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  const conflicts = new Set(data.conflicts.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
    if (conflicts.has(idx)) {
      inp.className = 'sudoku-cell conflict';
    }
  }
  if (data.solved) {
    stopTimer();
    if (!completionRecorded) {
      completionRecorded = true;
      addLeaderboardScore({
        name: document.getElementById('player-name').value.trim() || 'Anonymous',
        time: elapsedSeconds,
        difficulty: document.getElementById('difficulty').value,
        hints: data.hints_used
      });
    }
    msg.style.color = '#388e3c';
    msg.innerText = `Congratulations! You solved it in ${formatElapsedTime(elapsedSeconds)}!`;
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

async function requestHint() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = Array.from({length: SIZE}, (_, row) =>
    Array.from({length: SIZE}, (_, col) => {
      const value = inputs[row * SIZE + col].value;
      return value ? parseInt(value, 10) : 0;
    })
  );
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const idx = data.row * SIZE + data.col;
  inputs[idx].value = data.value;
  inputs[idx].disabled = true;
  inputs[idx].className = 'sudoku-cell prefilled';
  lockedCells = new Set(data.locked.map(([row, col]) => row * SIZE + col));
  hintsUsed = data.hints_used;
  msg.innerText = `Hint used: ${hintsUsed}`;
}

// Wire buttons
window.addEventListener('load', () => {
  applyTheme(loadTheme());
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint').addEventListener('click', requestHint);
  renderLeaderboard();
  // initialize
  newGame();
});