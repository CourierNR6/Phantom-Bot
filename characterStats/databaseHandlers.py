import logging

from characterStats.statTypes import TABLES
from database.db import get_element_by_id, query, update_element

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def fetch_table_columns():
    """Fetch column names for characters, attributes, save_mods, and skill_mods."""
    table_names = ["attributes", "save_mods", "skill_mods"]
    table_columns = {}

    for table in table_names:
        query_text = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s
            AND table_schema = 'public'
            ORDER BY ordinal_position;
        """

        result = await query(query_text, [table])
        if result:
            table_columns[table] = [row["column_name"] for row in result]
        else:
            logger.error(f"Failed to fetch columns for table: {table}")

    return table_columns

async def fetch_element_data(attributes_id: int, save_mods_id: int, skill_mods_id: int):
     # Fetch prefilled values from the database
    prefilled_values = {}

    # Fetch attributes data
    attributes_data = await get_element_by_id(list(TABLES.keys())[1], "*", attributes_id)
    if attributes_data:
        prefilled_values.update(
            {f"{list(TABLES.keys())[1]}_{key}": value for key, value in attributes_data[0].items()}
        )

    # Fetch save_mods data
    save_mods_data = await get_element_by_id(list(TABLES.keys())[2], "*", save_mods_id)
    if save_mods_data:
        prefilled_values.update(
            {f"{list(TABLES.keys())[2]}_{key}": value for key, value in save_mods_data[0].items()}
        )

    # Fetch skill_mods data
    skill_mods_data = await get_element_by_id(list(TABLES.keys())[3], "*", skill_mods_id)
    if skill_mods_data:
        prefilled_values.update(
            {f"{list(TABLES.keys())[3]}_{key}": value for key, value in skill_mods_data[0].items()}
        )

    return prefilled_values

async def update_sheet_database(reference_ids, responses):
    all_updated_tables = [f"{key.rsplit('_',1)[0]}" for key, value in responses.items()]
    all_updated_elements = [f"{key.rsplit('_',1)[1]}" for key, value in responses.items()]
    all_updated_values = [f"{value}" for key, value in responses.items()]
    current_table = all_updated_tables[0]
    updated_elements = []
    updated_values = []

    for i in range(len(all_updated_tables)):
        if current_table == all_updated_tables[i]:
            updated_elements.append(all_updated_elements[i])
            updated_values.append(all_updated_values[i])
        else:
            await update_element(current_table, reference_ids[TABLES[current_table]],
                updated_elements,
                updated_values
            )
            current_table = all_updated_tables[i]
            updated_elements = [all_updated_elements[i]]
            updated_values = [all_updated_values[i]]
        if i==(len(all_updated_tables)-1):
            await update_element(current_table, reference_ids[TABLES[current_table]],
                updated_elements,
                updated_values
            )

async def update_prefilled_values(reference_ids, interaction):
    prefilled_values = await fetch_element_data(reference_ids[1],reference_ids[2],reference_ids[3])
    if not prefilled_values:
        await interaction.response.send_message(
            "Failed to load prefilled character sheet data. Please try again later.", ephemeral=True
        )
    return prefilled_values
