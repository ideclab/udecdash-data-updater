PACKAGE_TABLES = (
    """ CREATE TABLE IF NOT EXISTS package_updates_instance (
            id SERIAL PRIMARY KEY,
            success_load INTEGER,
            failed_load INTEGER,
            created_at TIMESTAMP NOT NULL

            )
    """,
    """ CREATE TABLE IF NOT EXISTS package_files_loaded (
            id SERIAL PRIMARY KEY,
            instance INTEGER NOT NULL,
            table_name VARCHAR(256) NOT NULL,
            file_name VARCHAR(256) NOT NULL,
            status VARCHAR(100) NOT NULL,
            error_details TEXT,
            file_size BIGINT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP  NULL,
            updated_instance INTEGER
            )
    """,
    """ CREATE INDEX IF NOT EXISTS package_instace_index ON package_files_loaded(instance)
    """,
    """ CREATE INDEX IF NOT EXISTS package_table_name_index ON package_files_loaded(table_name)
    """,
)