const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Database setup
const db = new sqlite3.Database('chai_junction.db');

// Create tables
db.serialize(() => {
    // Recipes table
    db.run(`CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        image_url TEXT,
        customizations TEXT
    )`);

    // Orders table
    db.run(`CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        items TEXT NOT NULL,
        total_price REAL NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
});

// Routes
app.get('/api/recipes', (req, res) => {
    db.all('SELECT * FROM recipes', [], (err, rows) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(rows);
    });
});

app.post('/api/recipes', (req, res) => {
    const { name, description, price, category, image_url, customizations } = req.body;
    db.run(
        'INSERT INTO recipes (name, description, price, category, image_url, customizations) VALUES (?, ?, ?, ?, ?, ?)',
        [name, description, price, category, image_url, JSON.stringify(customizations)],
        function(err) {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.json({ id: this.lastID });
        }
    );
});

app.post('/api/orders', (req, res) => {
    const { customer_name, items, total_price } = req.body;
    db.run(
        'INSERT INTO orders (customer_name, items, total_price) VALUES (?, ?, ?)',
        [customer_name, JSON.stringify(items), total_price],
        function(err) {
            if (err) {
                res.status(500).json({ error: err.message });
                return;
            }
            res.json({ id: this.lastID });
        }
    );
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
}); 