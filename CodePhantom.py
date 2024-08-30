import discord
import random
import re
from discord.ext import commands
import commandsHandler
from rollType import SKILL, ATTRIBUTE, PROFICIENCY
from damageType import DAMAGE
from weaponType import WEAPON

token = "Token"

bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.command()
async def hello(ctx):
    await ctx.send("Hii There! I am the dnd Bot And Welcome to the discord.py tutorial")

@bot.tree.command(name="vorteil",description="Roll with advantage")
async def vorteil(interaction:discord.Interaction, modifier: int=0):
    await interaction.response.send_message(commandsHandler.vorteil(interaction.user, modifier))

@bot.tree.command(name="nachteil",description="Roll with disadvantage")
async def nachteil(interaction:discord.Interaction, modifier: int=0):
    await interaction.response.send_message(commandsHandler.nachteil(interaction.user, modifier))

@bot.tree.command(name="attribute",description="Roll for your attributes")
async def attribute(interaction:discord.Interaction):
    await interaction.response.send_message(commandsHandler.attribute())

@bot.listen()
async def on_message(message):

    input = message.content.lower()
    send = message.channel.send
    person = message.author.mention

    # Commands werden wir verfeinern
    # Roll Command
    if input.startswith('/roll'):
        command = re.sub(r'^/roll\s?', '', input).strip()
        match = re.match(r'^(\d+)?d\s?(\d+)\s?([+\-])?\s?(\d+)?\s?(.*)$', command)

        if match: #roll 1d20+12 fire

            # Generate roll elements
            dice = int(match.group(1) or '1')
            die_type = int(match.group(2))
            sign = match.group(3)
            additional_number = int(match.group(4) or '0')
            damage = match.group(5).strip()

            # Rolling
            rolls = [random.randint(1, die_type) for _ in range(dice)]
            if sign == '-':
                additional_number = -additional_number 
            result = sum(rolls) + additional_number

            # Generate Text
            ## Rolled Numbers to be hidden
            rolls_string = ", ".join(map(str, rolls))
            
            ## Add additional number if existing
            if additional_number!=0:
                sign = sign or "+"
                rolls_string += f"{sign} {abs(additional_number)}"
            
            ## Result
            if damage in DAMAGE:
                # du brauchst kein sign check mehr, weil du additoinal_number schon abhängig davon negativ gemacht hast und du kannst einfach sign selbst in den text hinzufügen
                send_string =  f'{person} Ergebnis: **{result}** {damage.capitalize()} Schaden [||{rolls_string}||]'
            else: # if not DAMAGE
                if dice == 1 and die_type == 20: 
                    # Dieser fall gilt eh nur bei 1 mal d20 ansonsten ist die antwort immer gleich
                    if 1 in rolls:
                        send_string = f'Nun {person} leider ist dies ein **kritischer Fehlschlag** doch bleiben Sie standhaft. Noch ist nichts verloren.\nErgebnis: **{result}** [||{rolls_string}||]'
            
                    elif 20 in rolls:
                        send_string = f'Meinen Glückwunsch für Ihren **kritischen Erfolg** {person}. Ich hoffe mit diesem Wurf kommen Sie weiter.\nErgebnis: **{result}** [||{rolls_string}||]'
            
                    else:
                        send_string = f'{person} Ergebnis: **{result}** [||{rolls_string}||]'        
                else:
                    send_string = f'{person} Ergebnis: **{result}** [||{rolls_string}||]'

        else:
            send_string = f'{person}, bitte gib einen gültigen Befehl ein, z.B. "/roll 2d6+3 Feuer" oder "/roll 1d20+5"'
        
        await send(send_string)
        
    # #Vorteil
    # elif input.startswith('/vorteil'):
    #     command = re.sub(r'^/vorteil\s?', '', input).strip()
    #     match = re.match(r'^\s?([+\-])?\s?(\d+)?$', command)

    #     if match:
    #         sign = match.group(1)
    #         additional_number = int(match.group(2) or '0')

    #         # Rolling        
    #         rolls = [random.randint(1, 20) for _ in range(2)]
    #         if sign == '-':
    #             additional_number = -additional_number
    #         advantage_rolls = max(rolls)
    #         result = advantage_rolls + additional_number

    #         # Generate Text
    #         ## Rolled Numbers to be hidden
    #         rolls_string = ", ".join(map(str, rolls))
    #         extra_text = ""
    #         extra_roll_text = ""

            
    #         ## Add additional number if existing
    #         if additional_number!=0:
    #             sign = sign or "+"
    #             rolls_string += f"{sign} {abs(additional_number)}"
    #             extra_roll_text = f" {sign} {abs(additional_number)}"

    #         ## Special cases
    #         if advantage_rolls == 1:  # Doppel 1
    #             extra_text = "Ich hoffe der Wurf war nicht wichtig "
    #         elif advantage_rolls == 20:  # Irgendeine Natürliche 20
    #             extra_text = "Meinen Glückwunsch für Ihren kritischen Erfolg "

    #         send_string = f"{extra_text}{person}: Ergebnis: **{result}** (||{advantage_rolls}{extra_roll_text}||) [||{rolls_string}||]"

    #     else:
    #         send_string = f'{person}, bitte gib einen gültigen Befehl ein, z.B. "/vorteil +3" oder "/vorteil"'
        
    #     await send(send_string)

    # #Nachteil
    # elif input.startswith('/nachteil'):
    #     command = re.sub(r'^/nachteil\s?', '', input).strip()
    #     match = re.match(r'^\s?([+\-])?\s?(\d+)?$', command)

    #     if match:
    #         sign = match.group(1)
    #         additional_number = int(match.group(2) or '0')
            
    #         # Rolling
    #         rolls = [random.randint(1, 20) for _ in range(2)]
    #         if sign == '-':
    #             additional_number = -additional_number
    #         disadvantage_rolls = min(rolls)
    #         result = disadvantage_rolls + additional_number

    #         rolls_string = ", ".join(map(str, rolls))
    #         extra_text = ""
    #         extra_roll_text = ""

    #         if additional_number!=0:
    #             sign = sign or "+"
    #             rolls_string += f"{sign} {abs(additional_number)}"
    #             extra_roll_text = f" {sign} {abs(additional_number)}"

    #         if disadvantage_rolls == 1:  # Doppel 1
    #             extra_text = "Das Glück ist Ihnen heute aber nicht hold "
    #         elif disadvantage_rolls == 20:  # Irgendeine Natürliche 20
    #             extra_text = "Ich glaube, ich traue meinen Augen gerade nicht, aber Sie haben gerade einen doppelten kritischen Erfolg erzielt. Chapeau!"

    #         send_string = f"{extra_text}{person}: Ergebnis: **{result}** (||{disadvantage_rolls}{extra_roll_text}||) [||{rolls_string}||]"

    #     else:
    #         send_string = f'{person}, bitte gib einen gültigen Befehl ein, z.B. "/nachteil -3" oder "/nachteil"'

    #     await send(send_string)

    # #Attribute
    # elif input == '/attribute':
    #     attributes = []
    #     ergebnis = 0
    #     for die_type in range(1, 7):
    #         rolls = sorted([random.randint(1, 6) for _ in range(4)])[0:]
    #         total = sum(rolls) - rolls[0]
    #         low = rolls[0]
    #         rolls[0]= "~~" + str(low) + "~~"
    #         attributes.append((rolls, total))
    #         ergebnis = ergebnis + total
    #     response = '\n'.join([f'Wert {i}: {rolls}. (**{total}**)' for i, (rolls, total) in enumerate(attributes, start=1)])

    #     await send(response + '\n'+ "Total = **" + str(ergebnis)+"**")
        
    #Fertigkeiten
    elif skill := next((key for rollType in [SKILL, ATTRIBUTE, PROFICIENCY] for key in sorted(rollType, key=len, reverse=True) if input.startswith(f"/{key}")), None):
        command = input[len(skill)+1:].strip()  # Initialisiere die Variable 'command' nach der fertigkeit
        match = re.match(r'^\s?([+\-])?\s?(\d+)?$', command)
        if match:
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
        
            skill_name = next(rollType[skill] for rollType in sorted((SKILL, ATTRIBUTE, PROFICIENCY), key=len, reverse=True) if skill in rollType)
            
            roll = random.randint(1, 20)
            result = roll + modifier 
            # wenn du was negatives addierst wird es eh automatisch substrahiert

            # Hier wird vorher Text generiert und erst danach gesendet
            show_rolled = f"_**{skill_name}:**_ **{result}** [||{roll}{extra_roll_text}||]"
            show_text = f"{person}\n"
            if roll == 1:
                show_text =f"Nun {person}, leider haben Sie einen kritischen Fehlschlag. Verzagen Sie nicht, es gibt immer andere Möglichkeiten.\n"
            elif roll == 20:
                show_text = f"Mein Glückwunsch {person}, Sie sind wohl sehr gut in dem, was Sie gerade machen. Beschreiben Sie, wie das aussieht, wenn es Ihnen gefällt.\n"
                
            await send(f'{show_text}{show_rolled}')
        else:
            await send(f'{person}, gib bitte einen gültigen Befehl ein, wie z.B. **/Charisma +5**.')

    #Waffen
    elif weapon := next((key for key in sorted(WEAPON, key=len, reverse=True) if input.startswith(f"/{key}")), None):
        command = input[len(weapon)+1:].strip()  # Initialisiere die Variable 'command'
        match = re.match(r'^\s?([+\-])?\s?(\d+)?$', command)
        if match:
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
        
            weapon_name = WEAPON[weapon]

            roll = random.randint(1, 20)
            result = roll + modifier 
            # wenn du was negatives addierst wird es eh automatisch substrahiert

            # Hier wird vorher Text generiert und erst danach gesendet
            show_rolled = f"_**{weapon_name}:**_ **{result}** [||{roll}{extra_roll_text}||]"
            show_text = f"{person}\n"
            if roll == 1:
                show_text =f"Nun {person}, leider haben Sie einen kritischen Fehlschlag. Verzagen Sie nicht, es gibt immer andere Möglichkeiten.\n"
            elif roll == 20:
                show_text = f"Mein Glückwunsch {person}, Sie sind wohl sehr gut in dem, was Sie gerade machen. Beschreiben Sie, wie das aussieht, wenn es Ihnen gefällt.\n"
                
            await send(f'{show_text}{show_rolled}')
        else:
            await send(f'{person}, gib bitte einen gültigen Befehl ein, wie z.B. **/Waffenlos +5**.')
    
bot.run(token)  

#Link: https://discord.com/oauth2/authorize?client_id=1276233268244517038&permissions=580997674773568&integration_type=0&scope=bot