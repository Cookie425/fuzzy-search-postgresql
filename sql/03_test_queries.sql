-- LIKE поиск
EXPLAIN ANALYZE
SELECT * FROM products
WHERE name LIKE '%laptop%';

-- LIKE с префиксом
EXPLAIN ANALYZE
SELECT * FROM products
WHERE name LIKE 'Del%';

-- ILIKE поиск
EXPLAIN ANALYZE
SELECT * FROM products
WHERE name ILIKE '%laptop%';

-- ILIKE с функциональным индексом
EXPLAIN ANALYZE
SELECT * FROM products
WHERE LOWER(name) LIKE LOWER('%laptop%');

-- Триграммный поиск
SET pg_trgm.similarity_threshold = 0.3;
EXPLAIN ANALYZE
SELECT *, similarity(name, 'laptop computer') AS sim FROM products
WHERE name % 'laptop computer'
ORDER BY sim DESC
LIMIT 10;

-- Поиск с опечаткой
EXPLAIN ANALYZE
SELECT * FROM products
WHERE name % 'laptop komputer';

-- Levenshtein distance
EXPLAIN ANALYZE
SELECT *, levenshtein(name, 'laptop computer') AS distance
FROM products
WHERE levenshtein(name, 'laptop computer') <= 3
ORDER BY distance
LIMIT 10;

-- Levenshtein с ограничением
EXPLAIN ANALYZE
SELECT *, levenshtein_less_equal(name, 'laptop computer', 3) AS distance
FROM products
WHERE levenshtein_less_equal(name, 'laptop computer', 3) <= 3
ORDER BY distance
LIMIT 10;

-- Soundex
EXPLAIN ANALYZE
SELECT * FROM products
WHERE soundex(name) = soundex('kompyuter');

-- Metaphone
EXPLAIN ANALYZE
SELECT *, metaphone(name, 10) AS phonetic
FROM products
WHERE metaphone(name, 10) = metaphone('kompyuter', 10);

-- Full-text search
EXPLAIN ANALYZE
SELECT *, ts_rank(search_vector, query) AS rank
FROM products, plainto_tsquery('english', 'laptop computer') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 10;