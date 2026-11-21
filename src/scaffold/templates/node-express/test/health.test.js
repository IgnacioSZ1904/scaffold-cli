import { test } from 'node:test';
import assert from 'node:assert/strict';
import { app } from '../src/app.js';

test('GET /health devuelve ok', async () => {
  const server = app.listen(0);
  const { port } = server.address();

  const response = await fetch('http://localhost:' + port + '/health');

  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { status: 'ok' });
  server.close();
});
