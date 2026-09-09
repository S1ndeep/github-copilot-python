const LEADERBOARD_STORAGE_KEY = 'sudoku.top10Scores.v1';
const MAX_LEADERBOARD_SIZE = 10;

function normalizeScores(value) {
  if (!Array.isArray(value)) return [];
  return value
    .filter((score) => score && typeof score === 'object')
    .map((score) => ({
      name: typeof score.name === 'string' && score.name.trim() ? score.name.trim() : 'Anonymous',
      time: Number(score.time),
      difficulty: typeof score.difficulty === 'string' ? score.difficulty : 'Medium',
      hints: Number(score.hints)
    }))
    .filter((score) => Number.isFinite(score.time) && score.time >= 0
      && Number.isInteger(score.hints) && score.hints >= 0)
    .sort((first, second) => first.time - second.time)
    .slice(0, MAX_LEADERBOARD_SIZE);
}

function loadLeaderboard() {
  try {
    return normalizeScores(JSON.parse(localStorage.getItem(LEADERBOARD_STORAGE_KEY) || '[]'));
  } catch (error) {
    return [];
  }
}

function saveLeaderboard(scores) {
  const normalized = normalizeScores(scores);
  try {
    localStorage.setItem(LEADERBOARD_STORAGE_KEY, JSON.stringify(normalized));
  } catch (error) {
    // Storage may be unavailable or full; the game can still be played.
  }
  return normalized;
}

function formatScoreTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const seconds = Math.floor(totalSeconds % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

function renderLeaderboard(scores = loadLeaderboard()) {
  const body = document.getElementById('leaderboard-body');
  if (!body) return;
  body.innerHTML = '';
  if (scores.length === 0) {
    const row = body.insertRow();
    const cell = row.insertCell();
    cell.colSpan = 4;
    cell.innerText = 'No completed games yet.';
    return;
  }
  scores.forEach((score) => {
    const row = body.insertRow();
    row.insertCell().innerText = score.name;
    row.insertCell().innerText = formatScoreTime(score.time);
    row.insertCell().innerText = score.difficulty;
    row.insertCell().innerText = score.hints;
  });
}

function addLeaderboardScore(score) {
  const scores = loadLeaderboard();
  scores.push(score);
  const topScores = saveLeaderboard(scores);
  renderLeaderboard(topScores);
  return topScores;
}