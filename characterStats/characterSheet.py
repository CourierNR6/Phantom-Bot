import logging
import math

import discord
from discord.ui import Button, Modal, TextInput, View

from characterStats.databaseHandlers import fetch_element_data, fetch_table_columns, update_prefilled_values, update_sheet_database

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def calculate_modifier(score:int, key:str):
    if not key.endswith("initiative"):
        logger.info(f"score was sent: {score}")
        modifier = math.floor((score - 10) / 2)
        logger.info(f"score's mod is: {modifier}")
    else:
        logger.info(f"initiative was sent: {score}")
        modifier = score
    return modifier

def calculate_passive(skill_modifier:str):
    logger.info(f"modifier was sent: {skill_modifier}")
    skill_mod = int(skill_modifier.replace(" ",""))
    passive_score = 10+skill_mod
    logger.info(f"skill's mod is: {passive_score}")
    return passive_score

class CharacterSheetModal(Modal):
    def __init__(self, table_columns:dict, prefilled_values:dict, name:str, pages:list, reference_ids:list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs = {}
        self.table_columns = table_columns
        self.prefilled_values = prefilled_values
        self.name = name
        self.pages = pages
        self.embed = {}
        self.reference_ids = reference_ids
        current_columns = []

        # Flatten table_columns into a list of columns
        flatten_all_tables(table_columns, current_columns)

        # Determine which columns to show on a page
        start_index = (pages[0] - 1) * 5
        end_index = start_index + 5
        page_columns = current_columns[start_index:end_index]

        self.create_modal(prefilled_values, page_columns)

    def create_modal(self, prefilled_values, page_columns):
        """Add the input fields for this page's columns."""
        for table, column in page_columns:
            # Skip unnecessary fields
            if not column.endswith("_id") and not column.endswith("_name") and column != "id":
                key = f"{table}_{column}"
                input_field = TextInput(
                    label=f"{table.capitalize().replace('_', ' ')} : {column.capitalize()}",
                    style=discord.TextStyle.short,
                    required=False,
                    default=str(prefilled_values.get(key, "_-_error_-_"))  # Prefill with existing value if available
                )
                self.add_item(input_field)
                self.inputs[key] = input_field

    async def on_submit(self, interaction: discord.Interaction):
        # Collect responses from the inputs
        responses = {key: input_field.value for key, input_field in self.inputs.items()}
        # Link related IDs back to the character

        await update_sheet_database(self.reference_ids, responses)
        await self.send_embed(interaction)

    async def send_embed(self, interaction: discord.Interaction):
        # Send a regular message with a button to trigger the next modal
        view = View()
        button = Button(label=f"Next Page {self.pages[0] + 1}/{self.pages[1]}", style=discord.ButtonStyle.primary)
        view.add_item(button)

        button.callback=self.send_next_modal

        self.prefilled_values = await update_prefilled_values(self.reference_ids, interaction)
        attributes, save_mods, passives, skill_mods_a_i, skill_mods_m_s = split_tables_to_fields(self.prefilled_values)

        self.embed = create_embed(self.name, attributes, save_mods, passives, skill_mods_a_i, skill_mods_m_s)

        user_mention = interaction.user.mention
        if self.pages[0] == 1:
            await interaction.response.send_message(
                f"{user_mention}! Character sheet for **{self.name}** has been updated **{self.pages[0]}/{self.pages[1]}**!",
                view=view,
                ephemeral=True,
                embeds=[self.embed]
            )
        elif self.pages[0] != self.pages[1]:
            await interaction.response.edit_message(
                content=f"{user_mention}! Character sheet for **{self.name}** has been updated **{self.pages[0]}/{self.pages[1]}**!",
                view=view,
                embeds=[self.embed]
            )
        else:
            await interaction.response.send_message(
                content=f"{user_mention}! Character sheet for **{self.name}** has been updated successfully!",
                embeds=[self.embed]
            )

    async def send_next_modal(self, interaction: discord.Interaction):
        # Prepare and send the next modal page
        next_page_number = self.pages[0] + 1

        self.prefilled_values = await update_prefilled_values(self.reference_ids, interaction)

        modal = CharacterSheetModal(
            table_columns=self.table_columns,
            prefilled_values=self.prefilled_values,
            name=self.name,
            pages=[next_page_number,self.pages[1]],
            reference_ids=[self.reference_ids[0],self.reference_ids[1],self.reference_ids[2],self.reference_ids[3]],
            title=f"Character Sheet: {self.name} {next_page_number}/{self.pages[1]}"
        )
        await interaction.response.send_modal(modal)

async def show_character_sheet(interaction: discord.Interaction, name: str,
                               character_id: int, attributes_id: int, save_mods_id: int, skill_mods_id: int):
    """Show the dynamic character sheet modal."""
    table_columns = await fetch_table_columns()
    if not table_columns:
        await interaction.response.send_message(
            "Failed to load character sheet data. Please try again later.", ephemeral=True
        )
        return

    reference_ids = [character_id, attributes_id, save_mods_id, skill_mods_id]
    prefilled_values = await update_prefilled_values(reference_ids, interaction)

    # Flatten all columns to calculate the total pages
    all_columns = []
    flatten_all_tables(table_columns, all_columns)

    # Calculate total pages (5 items per page) and start with 1
    total_pages = (len(all_columns) + 4) // 5
    current_page = 1

    # Initialize the modal with the first page
    modal = CharacterSheetModal(
        table_columns=table_columns,
        prefilled_values=prefilled_values,
        name = name,
        pages = [current_page, total_pages],
        reference_ids = reference_ids,
        title=f"Character Sheet: {name} 1/{total_pages}"
    )

    await interaction.response.send_modal(modal)

def flatten_all_tables(table_columns, all_columns):
    for table, columns in table_columns.items():
        for column in columns:
            if not column.endswith("_id") and not column.endswith("_name") and column != "id":
                all_columns.append((table, column))

def split_tables_to_fields(prefilled_values):
    attributes = [
        f"{key.replace('attributes_', '').title()}: {value} ({calculate_modifier(value, key)})"
        for key, value in prefilled_values.items()
        if key.startswith("attributes_") and not key.endswith("_id") and not key.endswith("_name") and key != "id"
    ]
    attributes = "\n".join(attributes) if attributes else "No attributes available."
    save_mods = [
        f"{key.replace('save_mods_', '').title()}: {value}"
        for key, value in prefilled_values.items()
        if key.startswith("save_mods_") and not key.endswith("_id") and not key.endswith("_name") and key != "id"
    ]
    save_mods = "\n".join(save_mods) if save_mods else "No attributes available."

    skill_mods = [
        f"{key.replace('skill_mods_', '').title()}: {value}"
        for key, value in prefilled_values.items()
        if key.startswith("skill_mods_") and not key.endswith("_id") and not key.endswith("_name") and key != "id"
    ]
    passives = f"Passive Perception: {calculate_passive(skill_mods[11][-2:])}\nPassive Insight: {calculate_passive(skill_mods[6][-2:])}\nPassive Investigation: {calculate_passive(skill_mods[8][-2:])}\n_Passive X: 10 + X_"

    # Filter and join items for the A-I range
    skill_mods_a_i = "\n".join(
        mod for mod in skill_mods if "A" <= mod[0] <= "I"
    ) or "No attributes available."

    # Filter and join items for the M-S range
    skill_mods_m_s = "\n".join(
        mod for mod in skill_mods if "M" <= mod[0] <= "S"
    ) or "No attributes available."

    return attributes,save_mods,passives,skill_mods_a_i,skill_mods_m_s

def create_embed(name, attributes, save_mods, passives, skill_mods_a_i, skill_mods_m_s):
    embed = discord.Embed(title=name, color=discord.Color.gold()) #,color=Hex code
    embed.add_field(name="Attributes", value=attributes, inline=True)
    embed.add_field(name="\t", value="\t", inline=True)
    embed.add_field(name="Save Mods", value=save_mods, inline=True)
    embed.add_field(name="Skill Mods [A-I]", value=skill_mods_a_i, inline=True)
    embed.add_field(name="\t", value="\t", inline=True)
    embed.add_field(name="Skill Mods [M-S]", value=skill_mods_m_s, inline=True)
    embed.add_field(name="Passive Skills", value=passives, inline=False)
    return embed
