const assert = require('node:assert/strict');
const fs = require('node:fs');
const test = require('node:test');
const vm = require('node:vm');

function createEnvironment(initialValue = null) {
  const storage = {
    value: initialValue,
    getItem() {
      return this.value;
    },
    setItem(_key, value) {
      this.value = value;
    },
  };
  const body = {
    rows: [],
    innerHTML: '',
    insertRow() {
      const row = {
        cells: [],
        insertCell() {
          const cell = {innerText: '', colSpan: 1};
          row.cells.push(cell);
          return cell;
        },
      };
      body.rows.push(row);
      return row;
    },
  };
  const context = {
    localStorage: storage,
    document: {
      getElementById() {
        return body;
      },
    },
  };
  vm.runInNewContext(
    fs.readFileSync('starter/static/leaderboard.js', 'utf8'),
    context,
  );
  return {context, storage, body};
}

function toNativeValue(value) {
  return JSON.parse(JSON.stringify(value));
}

test('leaderboard ignores corrupted localStorage data', () => {
  const {context} = createEnvironment('{not valid json');

  assert.deepEqual(toNativeValue(context.loadLeaderboard()), []);
});

test('leaderboard sorts scores and preserves score metadata', () => {
  const {context, storage} = createEnvironment();
  context.addLeaderboardScore({name: 'Slow', time: 120, difficulty: 'Hard', hints: 2});
  context.addLeaderboardScore({name: 'Fast', time: 45, difficulty: 'Easy', hints: 0});

  assert.deepEqual(toNativeValue(context.loadLeaderboard()), [
    {name: 'Fast', time: 45, difficulty: 'Easy', hints: 0},
    {name: 'Slow', time: 120, difficulty: 'Hard', hints: 2},
  ]);
  assert.match(storage.value, /Fast/);
});

test('leaderboard keeps only the ten best scores', () => {
  const {context} = createEnvironment();
  for (let time = 20; time >= 1; time -= 1) {
    context.addLeaderboardScore({
      name: `Player ${time}`,
      time,
      difficulty: 'Medium',
      hints: 1,
    });
  }

  const scores = toNativeValue(context.loadLeaderboard());
  assert.equal(scores.length, 10);
  assert.equal(scores[0].time, 1);
  assert.equal(scores[9].time, 10);
});
