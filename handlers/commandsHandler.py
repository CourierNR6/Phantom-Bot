
import random
import re, logging

import discord
from database.db import get_element_where, get_element_by_id, create_element, update_element
from customTypes import damageType
from characterStats.characterSheet import create_embed, show_character_sheet, split_tables_to_fields
from characterStats.databaseHandlers import update_prefilled_values

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def roll(user, roll_text, modifier_input, damage_input):

    match = re.match(r'^(\d+)?d\s?(\d+)\s?([+\-])?\s?(\d+)?\s?(.*)$', roll_text)

    dice_nr = int(match.group(1) or '1')
    die_type = int(match.group(2))

    sign_text = match.group(3)
    modifier_text = int(match.group(4) or '0')
    if modifier_input==0 and modifier_text!=0:
        modifier = -modifier_text if sign_text == '-' else modifier_text
    else:
        modifier = modifier_input

    damage = damage_input or match.group(5).strip()

    rolls = [random.randint(1, die_type) for _ in range(dice_nr)]
    result = sum(rolls) + modifier

    # Generate Text
    ## Rolled Numbers to be hidden
    rolls_string = ", ".join(map(str, rolls))
        
    ## Add additional number if existing
    if modifier!=0:
        sign = "+" if modifier > 0 else "-"
        rolls_string += f" {sign} {abs(modifier)}"
        
    ## Result
    if damage!="" and damage in damageType.DAMAGE:
        # du brauchst kein sign check mehr, weil du additoinal_number schon abhängig davon negativ gemacht hast und du kannst einfach sign selbst in den text hinzufügen
        send_string =  f'{user.mention} Ergebnis: **{result}** _{damage.capitalize()}_ Schaden [||{rolls_string}||]'
    elif damage!="" and not damage in damageType.DAMAGE:
        # Ich seh iwie nicht den grund damagatype checks zu machen. lass einfach den damage der eingegeben wurde immer ausgeben
        send_string =  f'{user.mention} Ergebnis: **{result}** _UNKNOWN {damage.capitalize()}_ Schaden [||{rolls_string}||]'
        
    else: # if not DAMAGE
        if dice_nr == 1 and die_type == 20: 
            # Dieser fall gilt eh nur bei 1 mal d20 ansonsten ist die antwort immer gleich
            if 1 in rolls:
                send_string = f'Nun {user.mention} leider ist dies ein **kritischer Fehlschlag** doch bleiben Sie standhaft. Noch ist nichts verloren.\nErgebnis: **{result}** [||{rolls_string}||]'
    
            elif 20 in rolls:
                send_string = f'Meinen Glückwunsch für Ihren **kritischen Erfolg** {user.mention}. Ich hoffe mit diesem Wurf kommen Sie weiter.\nErgebnis: **{result}** [||{rolls_string}||]'
    
            else:
                send_string = f'{user.mention} Ergebnis: **{result}** [||{rolls_string}||]'        
        else:
            send_string = f'{user.mention} Ergebnis: **{result}** [||{rolls_string}||]'
    
    return send_string

def vorteil(user, modifier):
        
    # Rolling
    rolls = [random.randint(1, 20) for _ in range(2)]
    
    disadvantage_rolls = max(rolls)
    result = disadvantage_rolls + modifier

    rolls_string = ", ".join(map(str, rolls))
    extra_text = ""
    extra_roll_text = ""

    if modifier!=0:
        sign = "+" if modifier > 0 else "-"
        rolls_string += f" {sign} {abs(modifier)}"
        extra_roll_text = f" {sign} {abs(modifier)}"

    if disadvantage_rolls == 1:  # Doppel 1
        extra_text = "Das Glück ist Ihnen heute aber nicht hold "
    elif disadvantage_rolls == 20:  # Irgendeine Natürliche 20
        extra_text = "Ich glaube, ich traue meinen Augen gerade nicht, aber Sie haben gerade einen doppelten kritischen Erfolg erzielt. Chapeau!"

    send_string = f"{extra_text}{user.mention}: Ergebnis: **{result}** (||{disadvantage_rolls}{extra_roll_text}||) [||{rolls_string}||]"

    return send_string


def nachteil(user, modifier):
        
    # Rolling
    rolls = [random.randint(1, 20) for _ in range(2)]
    
    disadvantage_rolls = min(rolls)
    result = disadvantage_rolls + modifier

    rolls_string = ", ".join(map(str, rolls))
    extra_text = ""
    extra_roll_text = ""

    if modifier!=0:
        sign = "+" if modifier > 0 else "-"
        rolls_string += f" {sign} {abs(modifier)}"
        extra_roll_text = f" {sign} {abs(modifier)}"

    if disadvantage_rolls == 1:  # Doppel 1
        extra_text = "Das Glück ist Ihnen heute aber nicht hold "
    elif disadvantage_rolls == 20:  # Irgendeine Natürliche 20
        extra_text = "Ich glaube, ich traue meinen Augen gerade nicht, aber Sie haben gerade einen doppelten kritischen Erfolg erzielt. Chapeau!"

    send_string = f"{extra_text}{user.mention}: Ergebnis: **{result}** (||{disadvantage_rolls}{extra_roll_text}||) [||{rolls_string}||]"

    return send_string

def attribute():
    attributes = []
    ergebnis = 0
    for trials in range(1, 7):
        rolls = sorted([random.randint(1, 6) for _ in range(4)])[0:]
        total = sum(rolls) - rolls[0]
        low = rolls[0]
        rolls[0]= "~~" + str(low) + "~~"
        attributes.append((rolls, total))
        ergebnis = ergebnis + total
        
    response = '\n'.join([f'Wert {i}: {rolls}. (**{total}**)' for i, (rolls, total) in enumerate(attributes, start=1)])
    send_string = f'{response}\nTotal = **{str(ergebnis)}**'
    
    return send_string

def weaponRoll(weapon, extra, user):
    match = re.match(r'^\s?([+\-])?\s?(\d+)?$', extra)
    sign = match.group(1)
    modifier = int(match.group(2) or '0')
    
    # Rolling
    roll = random.randint(1, 20)
    if sign == '-':
        modifier = -modifier
    result = roll + modifier

    extra_roll_text = ""

    if modifier!=0:
        sign = sign or "+"
        extra_roll_text = f" {sign} {abs(modifier)}"

    roll = random.randint(1, 20)
    result = roll + modifier 
    # wenn du was negatives addierst wird es eh automatisch substrahiert

    # Hier wird vorher Text generiert und erst danach gesendet
    show_rolled = f"_**{weapon}:**_ **{result}** [||{roll}{extra_roll_text}||]"
    show_text = f"{user.mention}\n"
    if roll == 1:
        show_text =f"Nun {user.mention}, leider haben Sie einen kritischen Fehlschlag. Verzagen Sie nicht, es gibt immer andere Möglichkeiten.\n"
    elif roll == 20:
        show_text = f"Mein Glückwunsch {user.mention}, Sie sind wohl sehr gut in dem, was Sie gerade machen. Beschreiben Sie, wie das aussieht, wenn es Ihnen gefällt.\n"

    send_text = f'{show_text}{show_rolled}'

    return send_text


def skillRoll(skill, extra, user):
    match = re.match(r'^\s?([+\-])?\s?(\d+)?$', extra)
    sign = match.group(1)
    modifier = int(match.group(2) or '0')
    
    # Rolling
    roll = random.randint(1, 20)
    if sign == '-':
        modifier = -modifier
    result = roll + modifier

    extra_roll_text = ""

    if modifier!=0:
        sign = sign or "+"
        extra_roll_text = f" {sign} {abs(modifier)}"

    roll = random.randint(1, 20)
    result = roll + modifier 
    # wenn du was negatives addierst wird es eh automatisch substrahiert

    # Hier wird vorher Text generiert und erst danach gesendet
    show_rolled = f"_**{skill}:**_ **{result}** [||{roll}{extra_roll_text}||]"
    show_text = f"{user.mention}\n"
    if roll == 1:
        show_text =f"Nun {user.mention}, leider haben Sie einen kritischen Fehlschlag. Verzagen Sie nicht, es gibt immer andere Möglichkeiten.\n"
    elif roll == 20:
        show_text = f"Mein Glückwunsch {user.mention}, Sie sind wohl sehr gut in dem, was Sie gerade machen. Beschreiben Sie, wie das aussieht, wenn es Ihnen gefällt.\n"

    send_text = f'{show_text}{show_rolled}'

    return send_text

def create_dynamic_dic_command(key, value):
    async def dyn_cmd(ctx):
        user = ctx.author
        mention = user.mention

        # Check if egg_message is callable (like the test function)
        if callable(value):
            value_result = value()  # Execute the function to get the result
        else:
            value_result = value  # Use as is if not callable

        send_text = f'{mention} {value_result}'
        await ctx.send(send_text)

    return dyn_cmd

async def setStats(interaction, user_id, name):

    character = None
    attributes = None
    saves = None
    skills = None
    character = await get_element_where('characters', '*', 'name', name)
    if character:
        logger.info(f"Character with name {name} exists")
        # Fetch related attributes
        attributes = await get_element_where('attributes', '*', 'character_id', character[0]["id"])
        saves = await get_element_where('save_mods', '*', 'character_id', character[0]["id"])
        skills = await get_element_where('skill_mods', '*', 'character_id', character[0]["id"])

        # Ensure all related entries were created successfully
        if not (attributes and saves and skills):
            logger.error("Failed to fetch related entries for character.")
            await interaction.response.send_message("Error fetching character details.", ephemeral=True)
            return
    else:
        logger.info(f"Character with name {name} is being created")
        # Create the main character entry
        character = await create_element('characters',
            ['name', 'user_id'],
            [name, user_id]
        )
        if not character:
            logger.error("Failed to create character.")
            await interaction.response.send_message("Error creating character.", ephemeral=True)
            return

        # Create related entries in attributes, saves, and skills tables
        attributes = await create_element('attributes',
            ['character_name', 'character_id'],
            [name, character[0]["id"]]
        )
        saves = await create_element('save_mods',
            ['character_name', 'character_id'],
            [name, character[0]["id"]]
        )
        skills = await create_element('skill_mods',
            ['character_name', 'character_id'],
            [name, character[0]["id"]]
        )

        # Ensure all related entries were created successfully
        if not (attributes and saves and skills):
            logger.error("Failed to create related entries for character.")
            await interaction.response.send_message("Error creating character details.", ephemeral=True)
            return

        # Link related IDs back to the character
        updated = await update_element('characters', character[0]["id"],
            ['attributes_id', 'save_mods_id', 'skill_mods_id'],
            [attributes[0]["id"], saves[0]["id"], skills[0]["id"]]
        )
        if not updated:
            logger.error("Failed to update character with related IDs.")
            await interaction.response.send_message("Error finalizing character creation.", ephemeral=True)
            return

    await show_character_sheet(interaction, name, character[0]["id"], attributes[0]["id"], saves[0]["id"], skills[0]["id"])
    return
