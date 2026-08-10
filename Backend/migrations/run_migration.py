import psycopg2

conn = psycopg2.connect(
    dbname='demand_forecast_states',
    user='ra_admin',
    password='admin',
    host='localhost',
    port='5432'
)
conn.autocommit = True
cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS public.api_keys
    (
        id          SERIAL PRIMARY KEY,
        api_key     TEXT        UNIQUE NOT NULL,
        owner_name  TEXT        NOT NULL,
        is_active   BOOLEAN     DEFAULT TRUE,
        created_at  TIMESTAMP   DEFAULT NOW()

    );
""")
print("Table 'api_keys' created.")

# Create index
cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_api_keys_key ON public.api_keys (api_key);
""")
print("Index 'idx_api_keys_key' created.")

# Create view (compatible with older PostgreSQL versions)
cur.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_views WHERE viewname = 'active_api_keys') THEN
            EXECUTE '
                CREATE VIEW active_api_keys AS
                SELECT id, owner_name, api_key, created_at
                FROM   api_keys
                WHERE  is_active = TRUE
            ';
        END IF;
    END $$;
""")
print("View 'active_api_keys' created.")

print("\nMigration completed successfully!")
cur.close()
conn.close()
