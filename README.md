# Аннотация  
Проект посвящен реализации и сравнению методов нечеткого поиска в PostgreSQL для работы с неточными и ошибочными запросами. Рассматриваются основные подходы: поиск по шаблонам (LIKE/ILIKE), триграммный анализ (pg_trgm), расстояние Левенштейна, фонетические алгоритмы (Soundex, Metaphone) и полнотекстовый поиск (FTS). Включает генерацию тестовых данных с искусственными опечатками, оптимизацию запросов через индексы, бенчмаркинг производительности и анализ точности каждого метода. Результаты помогают выбрать оптимальный способ поиска для разных сценариев.

# Запуск проекта

Для запуска проекта необходимо

### 0. Установить зависимости requirements.txt

### 1. Создать базу данных Posgres;

### 2. Создать файл .env в корне проекта и добавить в него переменные окружения для подключения к PostgreSQL:
DB_HOST=  
DB_PORT=  
DB_NAME=  
DB_USER=  
DB_PASSWORD=  

### 3. В базе PostgreSQL при помощи команды:  
`\i '`{ПУТЬ К ПРОЕКТУ}`\\fuzzy-search-postgresql\\sql\\01_create_schema.sql'`  
Создать структуру базы.

### 4. Заполнить таблицу тестовыми данными:  
`fuzzy-search-postgresql\scripts\generate_data\generate_data.py`  

### 5. Создать индексацию для таблиц при помощи команды:  
`\i '`{ПУТЬ К ПРОЕКТУ}`\\fuzzy-search-postgresql\\sql\\02_create_indexes.sql'`  

### 6. Создать SQL функция для проведения тестов:  
`\i '`{ПУТЬ К ПРОЕКТУ}`\\fuzzy-search-postgresql\\sql\\04_benchmarks.sql'`  

### 7. Запустить тестирование "benchmark":  
`fuzzy-search-postgresql\scripts\generate_data\run_benchmarks.py`  

### 8. Выполнить создание графиков результатов анализа:  
`fuzzy-search-postgresql\scripts\analyze_results\analyze_results.py`  


# Описание структуры проекта

### Папка data:  
Содержит текущую базу данных test_data.csv и данные результатов её анализа benchmark_results.csv  

### Папка results:  
Содержит папку accuracy_metrics с результатами анализа точности используемых методов  
Содержит папку performance_metrics с результатами анализа производительности используемых методов  
Общую таблицу результатов анализа: summary_table.xlsx  

### Папка sql:  
01_create_schema.sql - для создание структуры БД  
02_create_indexes.sql - для индексирования таблиц БД  
03_test_queries.sql - для проведения "EXPLAIN ANALYZE"  
04_benchmarks.sql - создание sql функции для проведения тестов  

### Папка scripts:
Содержит 3 раздела, каждый раздел отвественнен за определенный функционал.  
generate_data - генерация данных  
run_benchmarks - проведение тестов  
analyze_results - вывод результатов  

