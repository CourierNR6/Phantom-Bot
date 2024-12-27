import logging
import os

from psycopg2 import connect, sql

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DB_PARAMS = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT")),
}

# Function to establish a database connection
def get_db_connection():
    try:
        conn = connect(**DB_PARAMS)
        return conn
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        raise

# Function to initiate tables
def initiate_tables(conn):
    table_definitions = [
        {
            "name": "characters",
            "schema": """
                (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    user_id BIGINT,
                    attributes_id INT,
                    save_mods_id INT,
                    skill_mods_id INT,
                    FOREIGN KEY (attributes_id) REFERENCES attributes(id),
                    FOREIGN KEY (save_mods_id) REFERENCES save_mods(id),
                    FOREIGN KEY (skill_mods_id) REFERENCES skill_mods(id)
                )
            """
        },
        {
            "name": "attributes",
            "schema": """
                (
                    id SERIAL PRIMARY KEY,
                    character_name VARCHAR(255) NOT NULL,
                    character_id INT NOT NULL,

                    strength INT NOT NULL DEFAULT 10,
                    dexterity INT NOT NULL DEFAULT 10,
                    constitution INT NOT NULL DEFAULT 10,
                    intelligence INT NOT NULL DEFAULT 10,
                    wisdom INT NOT NULL DEFAULT 10,
                    charisma INT NOT NULL DEFAULT 10,

                    initiative INT NOT NULL DEFAULT 0
                )
            """
        },
        {
            "name": "save_mods",
            "schema": """
                (
                    id SERIAL PRIMARY KEY,
                    character_name VARCHAR(255) NOT NULL,
                    character_id INT NOT NULL,

                    strength INT NOT NULL DEFAULT 0,
                    dexterity INT NOT NULL DEFAULT 0,
                    constitution INT NOT NULL DEFAULT 0,
                    intelligence INT NOT NULL DEFAULT 0,
                    wisdom INT NOT NULL DEFAULT 0,
                    charisma INT NOT NULL DEFAULT 0,

                    death INT NOT NULL DEFAULT 0
                )
            """
        },
        {
            "name": "skill_mods",
            "schema": """
                (
                    id SERIAL PRIMARY KEY,
                    character_name VARCHAR(255) NOT NULL,
                    character_id INT NOT NULL,

                    acrobatics INT NOT NULL DEFAULT 0,
                    animal INT NOT NULL DEFAULT 0,
                    arcana INT NOT NULL DEFAULT 0,
                    athletics INT NOT NULL DEFAULT 0,
                    deception INT NOT NULL DEFAULT 0,
                    history INT NOT NULL DEFAULT 0,
                    insight INT NOT NULL DEFAULT 0,
                    intimidation INT NOT NULL DEFAULT 0,
                    investigation INT NOT NULL DEFAULT 0,
                    medicine INT NOT NULL DEFAULT 0,
                    nature INT NOT NULL DEFAULT 0,
                    perception INT NOT NULL DEFAULT 0,
                    performance INT NOT NULL DEFAULT 0,
                    persuasion INT NOT NULL DEFAULT 0,
                    religion INT NOT NULL DEFAULT 0,
                    sleight INT NOT NULL DEFAULT 0,
                    stealth INT NOT NULL DEFAULT 0,
                    survival INT NOT NULL DEFAULT 0
                )
            """
        },
    ]
    cursor = conn.cursor()  # Create a cursor object
    try:
        for table in table_definitions:
            query = sql.SQL("CREATE TABLE IF NOT EXISTS {} {}").format(
                sql.Identifier(table["name"]),
                sql.SQL(table["schema"])
            )
            cursor.execute(query)
            conn.commit()
            logger.info(f"Table '{table['name']}' created or already exists.")
    except Exception as e:
        logger.error(f"Error creating the tables: {e}")
    finally:
        cursor.close()  # Close the cursor
        conn.close()  # Close the connection

# Call the functions to test them
conn = get_db_connection()
initiate_tables(conn)
