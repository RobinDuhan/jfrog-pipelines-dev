const express = require('express');
const request = require('request-promise'); // Add this line
const bodyParser = require('body-parser');
const morgan = require('morgan');

const app = express();

app.use(morgan('dev'));
app.use(bodyParser.json());

app.get('/', async (req, res) => {
  try {
    const response = await request('https://www.example.com'); // Use request-promise
    res.send(`Response from external website: ${response}`);
  } catch (error) {
    console.error('Error:', error.message);
    res.status(500).send('Internal server error');
  }
});