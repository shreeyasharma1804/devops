const express = require('express');
const app = express();
const healthcheck = require('express-healthcheck');

const port = 3000;

app.use('/health', healthcheck());

app.get('/', (req, res) => {
  res.send('hello');
});

app.get('/headers', (req, res) => {
  res.json(req.headers);
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});

// node index.js