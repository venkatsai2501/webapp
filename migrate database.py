import sqlite3
import psycopg2
from psycopg2.extras import execute_values

# SQLite database path
sqlite_db = "db.sqlite3"

# PostgreSQL connection details
pg_host = "localhost"
pg_dbname = "pmdb"
pg_user = "postgres"
pg_password = "postgres"

def migrate_sqlite_to_postgres(sqlite_db, pg_host, pg_dbname, pg_user, pg_password):
    # Connect to SQLite
    sqlite_conn = sqlite3.connect(sqlite_db)
    sqlite_cursor = sqlite_conn.cursor()

    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(
        host=pg_host,
        database=pg_dbname,
        user=pg_user,
        password=pg_password
    )
    pg_cursor = pg_conn.cursor()

    # Get list of tables in SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()

    for table_name, in tables:
        print(f"Processing table: {table_name}")
        
        # Fetch SQLite table schema
        sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
        columns = sqlite_cursor.fetchall()
        column_names = [col[1] for col in columns]  # Get column names

        # Fetch all data from SQLite table
        sqlite_cursor.execute(f"SELECT * FROM {table_name};")
        rows = sqlite_cursor.fetchall()

        # Create a corresponding table in PostgreSQL
        columns_sql = ", ".join(
            [f'"{col[1]}" {sqlite_to_postgres_type(col[2])}' for col in columns]
        )
        pg_cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_sql});')

        # Insert data into PostgreSQL table
        if rows:
            placeholders = ", ".join([f"%s" for _ in column_names])
            insert_query = f'INSERT INTO "{table_name}" ({", ".join(column_names)}) VALUES %s'
            execute_values(pg_cursor, insert_query, rows)  # Bulk insert using execute_values

    # Commit and close connections
    pg_conn.commit()
    pg_cursor.close()
    pg_conn.close()
    sqlite_cursor.close()
    sqlite_conn.close()
    print("Data migration completed!")

def sqlite_to_postgres_type(sqlite_type):
    """Map SQLite types to PostgreSQL types."""
    mapping = {
        "TEXT": "VARCHAR",
        "INTEGER": "INT",
        "REAL": "FLOAT",
        "BLOB": "BYTEA",
        "NUMERIC": "DECIMAL",
    }
    return mapping.get(sqlite_type.upper(), "TEXT")  # Default to TEXT

# Run migration
migrate_sqlite_to_postgres(sqlite_db, pg_host, pg_dbname, pg_user, pg_password)
