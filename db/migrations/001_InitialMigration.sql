CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    summary TEXT NOT NULL,
    title TEXT,
    topics TEXT[] NOT NULL,
    sentiment TEXT NOT NULL,
    keywords TEXT[] NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
