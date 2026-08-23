CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    period TEXT NOT NULL,
    region TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0)
);

INSERT INTO sales (period, region, amount) VALUES
    ('current', 'North', 120000),
    ('current', 'South', 95000),
    ('current', 'West', 80000),
    ('previous', 'North', 150000),
    ('previous', 'South', 110000),
    ('previous', 'West', 90000);
