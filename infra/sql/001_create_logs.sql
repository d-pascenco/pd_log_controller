CREATE TABLE IF NOT EXISTS logs (
    id         SERIAL PRIMARY KEY,
    message    VARCHAR NOT NULL,
    level      VARCHAR NOT NULL,
    source     VARCHAR NOT NULL,
    timestamp  TIMESTAMP DEFAULT NOW()
);
