-- sql/schema.sql
CREATE TABLE banks (
  bank_id SERIAL PRIMARY KEY,
  bank_name VARCHAR(100) UNIQUE,
  app_id VARCHAR(200)
);

CREATE TABLE reviews (
  review_id SERIAL PRIMARY KEY,
  bank_id INT REFERENCES banks(bank_id),
  review_text TEXT,
  rating INT,
  review_date DATE,
  sentiment_label VARCHAR(10),
  sentiment_score NUMERIC,
  topic INT,
  source VARCHAR(50)
);
