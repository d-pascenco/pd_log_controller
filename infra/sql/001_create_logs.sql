CREATE TABLE IF NOT EXISTS logs (
    id         SERIAL PRIMARY KEY,
    source     VARCHAR NOT NULL,
    timestamp  TIMESTAMP DEFAULT NOW(),
    level      VARCHAR NOT NULL,
    message    VARCHAR NOT NULL,
);
