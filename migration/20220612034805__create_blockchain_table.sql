CREATE TABLE blockchain (
    id INTEGER PRIMARY KEY,
    data TEXT NULL,
    hash TEXT NOT NULL,
    nonce INTEGER NULL,
    created_at TIMESTAMP NOT NULL
);

INSERT INTO blockchain (
    id,
    data,
    hash,
    nonce,
    created_at
) VALUES (
    0,
    '{"transactions": []}',
    '8f829e9831c36d9e6c1140252048c749ff29bfff1ec7bb38bc3a18d356e504a2',
    null,
    '2022-06-12T04:49:16.425598'
);
