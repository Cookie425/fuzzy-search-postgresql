CREATE OR REPLACE FUNCTION analyze_query_plan(query_text TEXT)
RETURNS TABLE(
    node_type TEXT,
    index_name TEXT,
    startup_cost FLOAT,
    total_cost FLOAT,
    rows BIGINT
) AS $$
DECLARE
    plan_json JSON;
BEGIN
    EXECUTE 'EXPLAIN (FORMAT JSON) ' || query_text INTO plan_json;
    
    -- Возвращаем результаты из подпланов (Plans)
    RETURN QUERY
    SELECT 
        j->>'Node Type' AS node_type,
        j->>'Index Name' AS index_name,
        (j->>'Startup Cost')::FLOAT AS startup_cost,
        (j->>'Total Cost')::FLOAT AS total_cost,
        (j->>'Plan Rows')::BIGINT AS rows
    FROM json_array_elements(plan_json->0->'Plan'->'Plans') AS j;
    
    -- Возвращаем результаты из основного плана
    RETURN QUERY
    SELECT 
        plan_json->0->'Plan'->>'Node Type' AS node_type,
        plan_json->0->'Plan'->>'Index Name' AS index_name,
        (plan_json->0->'Plan'->>'Startup Cost')::FLOAT AS startup_cost,
        (plan_json->0->'Plan'->>'Total Cost')::FLOAT AS total_cost,
        (plan_json->0->'Plan'->>'Plan Rows')::BIGINT AS rows;
END;
$$ LANGUAGE plpgsql;