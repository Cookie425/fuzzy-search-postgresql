-- Подключение расширений
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

-- Создание основной таблицы
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,     -- Название товара (может содержать опечатки)
    description TEXT,               -- Подробное описание товара
    category VARCHAR(100),          -- Категория товара
    brand VARCHAR(100),             -- Бренд производителя
    sku VARCHAR(50) UNIQUE          -- Уникальный артикул товара
);

-- Создание таблицы тестовых запросов
CREATE TABLE test_queries (
    id SERIAL PRIMARY KEY,
    correct_term VARCHAR(255),      -- Корректный поисковый термин (например, "laptop")
    typo_term VARCHAR(255),         -- Версия термина с опечаткой (например, "latop")
    error_type VARCHAR(50)          -- 'transposition', 'deletion', 'insertion', 'substitution'
);

-- Создание таблицы для логирования результатов
CREATE TABLE search_benchmarks (
    id SERIAL PRIMARY KEY,
    method VARCHAR(50),             -- Метод/алгоритм поиска, который тестировался (например, "fulltext", "trigram", "vector")
    dataset_size INTEGER,           -- Размер тестового набора данных (количество записей)
    query_text VARCHAR(255),        -- Текст поискового запроса, который выполнялся
    execution_time_ms FLOAT,        -- Время выполнения запроса в миллисекундах
    result_count INTEGER,           -- Количество найденных результатов
    test_run_id UUID,               -- Уникальный идентификатор тестового прогона (для группировки результатов)
    cpu_usage FLOAT,                -- Загрузка CPU во время выполнения запроса (%)
    memory_usage FLOAT,             -- Использование памяти во время выполнения запроса (MB)
    total_relevant INT,             -- Общее количество релевантных результатов
    error_type VARCHAR(50),         -- Тип ошибки ввода при запросе
    index_used BOOLEAN,             -- Использовался ли индекс при поиске (true/false)
    is_typo BOOLEAN,                -- Был ли запрос с опечаткой
    plan_analysis JSONB             -- Анализ
);

-- Таблица связей запросов и товаров
CREATE TABLE query_product_matches (
    id SERIAL PRIMARY KEY,
    query_id INTEGER NOT NULL REFERENCES test_queries(id),  -- ID тестового запроса (внешний ключ)
    sku TEXT[] NOT NULL                                     -- Массив sku кодов
);

-- Таблица ожидаемых результатов тестов
CREATE TABLE benchmark_expected_results (
    id SERIAL PRIMARY KEY,
    benchmark_id INTEGER NOT NULL REFERENCES search_benchmarks(id), -- ID поля теста (внешний ключ)
    expected_skus TEXT[] NOT NULL                                   -- Массив sku кодов
);

-- Примеры тестовых данных
INSERT INTO test_queries (correct_term, typo_term, error_type) VALUES
('laptop', 'latpop', 'transposition'),
('computer', 'compter', 'deletion'),
('keyboard', 'keyboard', 'transposition'),
('monitor', 'monitor', 'insertion'),
('mouse', 'mause', 'substitution');