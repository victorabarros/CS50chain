CREATE TABLE blockchain (
    id INTEGER PRIMARY KEY,
    data TEXT NOT NULL,
    hash TEXT NOT NULL,
    nonce INTEGER NOT NULL,
    created_at TIMESTAMP
);
