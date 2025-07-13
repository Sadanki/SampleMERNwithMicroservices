const express = require('express');
require('dotenv').config();
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000; // Default port if not specified

app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {
  res.json({ msg: 'Hello World' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'OK' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('Shutting down gracefully');
  process.exit(0);
});

app.listen(port, () => {
  console.log(`Hello service running on port ${port}`);
});