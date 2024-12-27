import logging

from psycopg2.extras import RealDictCursor

from .dbConfig import get_db_connection

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Function to execute a query
async def query(text, params=None):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            conn.autocommit = False
            cursor.execute("BEGIN")
            cursor.execute(text, params)  # Use params as a list or tuple
            conn.commit()
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Database query error: {e}")
        conn.rollback()
        return None  # Return None to indicate failure
    finally:
        conn.close()

# Function to create a new element in a table
async def create_element(table, columns, values):
    placeholders = ", ".join(["%s" for _ in columns])  # Use %s placeholders
    query_text = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders}) RETURNING *"
    result = await query(query_text, values)
    check_faulty_result(table, result)
    return result

# Function to get an element by ID
async def get_element_by_id(table, element, id):
    result = await query(f"SELECT {element} FROM {table} WHERE id = %s", [id])
    check_faulty_result(table, result)
    return result


# Function to get an element based on a condition
async def get_element_where(table, element, where, value):
    result = await query(f"SELECT {element} FROM {table} WHERE {where} = %s", [value])
    check_faulty_result(table, result)
    return result

# Function to update an element by ID
async def update_element(table, id, columns, values):
    set_clause = ", ".join([f"{col} = %s" for col in columns])  # Use %s placeholders
    query_text = f"UPDATE {table} SET {set_clause} WHERE id = %s RETURNING *"
    result = await query(query_text, values + [id])
    check_faulty_result(table, result)
    return result

# Check if the result is faulty
def check_faulty_result(table, result):
    if result is None:  # Check if result is None (query failure)
        logger.error(f"Failed to take action in table: {table}")

# Function to check if a table is empty
async def is_table_empty(table):
    result = await query(f"SELECT COUNT(*) FROM {table}")
    check_faulty_result(table, result)
    return result["count"] == "0"

# Function to delete an element by ID
async def delete_element(table, id):
    result = await query(f"DELETE FROM {table} WHERE id = %s RETURNING *", [id])
    check_faulty_result(table, result)
    return result

# Function to empty a table
async def empty_table(table):
    result = await query(f"TRUNCATE TABLE {table} CASCADE;")
    check_faulty_result(table, result)
    return result

