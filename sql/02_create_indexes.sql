-- LIKE с префиксом
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);

-- ILIKE с функциональным индексом
CREATE INDEX IF NOT EXISTS idx_products_name_lower ON products(LOWER(name));

-- Триграммный индекс
CREATE INDEX IF NOT EXISTS idx_products_name_trgm ON products USING gin (SUBSTRING(name, 1, 1000) gin_trgm_ops);

-- Soundex индекс
CREATE INDEX IF NOT EXISTS idx_products_name_soundex ON products(soundex(name));

-- Full-text search индекс
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_attribute WHERE attrelid = 'products'::regclass AND attname = 'search_vector') THEN
        ALTER TABLE products ADD COLUMN search_vector tsvector;
        
        UPDATE products
        SET search_vector = to_tsvector('english',
            coalesce(name, '') || ' ' ||
            coalesce(description, '') || ' ' ||
            coalesce(category, ''));
        
        CREATE INDEX IF NOT EXISTS idx_products_fts ON products USING gin(search_vector);
    END IF;
END $$;
