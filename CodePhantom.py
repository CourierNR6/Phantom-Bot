import discord
import random
import re
from discord.ext import commands

client = discord.Client(intents=discord.Intents.all())
token = "Token"
@client.event


async def on_message(message):

    c = message.content.lower()
    send = message.channel.send
    person = message.author.mention
    if c.startswith('/roll') or c.startswith('/Roll'):
        command = re.sub(r'^/roll\s?', '', c).strip()
        match = re.match(r'^(\d+)?\s?([<>]?)\s?d\s?(\d+)\s?([+\-])?\s?(\d+)?\s?(.*)$', command)

        if match: #roll 1d20+12 fire
            n = int(match.group(1) or '1')
            op = match.group(2)
            i = int(match.group(3))
            sign = match.group(4)
            j = int(match.group(5) or '0')
            damage = match.group(6).strip()
            rolls = [random.randint(1, i) for _ in range(n)]
            if sign == '-':
                j = -j


            if op == '>':
                result = max(rolls) + j
                rolls_str = f"{', '.join(map(str, rolls))}"
                rolls_str += f", **{max(rolls)}**"
            elif op == '<':
                result = min(rolls) + j
                rolls_str = f"{', '.join(map(str, rolls))}"
                rolls_str += f", **{min(rolls)}**"
            else:
                result = sum(rolls) + j
                rolls_str = ", ".join(map(str, rolls))
            
            if damage:
                if damage.lower() in ['acid', 'bludgeoning', 'cold', 'fire', 'force', 'lightning', 'necrotic', 'piercing', 'poison', 'psychic', 'radiant', 'slashing', 'thunder', 'säure', 'wucht', 'kälte', 'feuer', 'energie', 'blitz', 'nekrotisch', 'stich', 'gift', 'psychisch', 'gleißend', 'hieb', 'donner']:
                    if sign == '+':
                        if j == 0: #Modifikator ist 0
                            await send(f'{person} Ergebnis: **{result}** {damage.capitalize()}schaden [||{rolls_str}||])')
                        else:
                            await send(f'{person} Ergebnis: **{result}** {damage.capitalize()}schaden [||{rolls_str} + {j}||])')
                    else:
                        if j == 0: #Modifikator ist 0
                            await send(f'{person} Ergebnis: **{result}** {damage.capitalize()}schaden [||{rolls_str}||])')
                        else:
                            await send(f'{person} Ergebnis: **{result}** {damage.capitalize()}schaden [||{rolls_str} - {j}||])')
                
            else:
                if sign == '-':
                    j = -j
                    if n == 1:
                        if i == 20:
                            if 1 in rolls:
                                if j == 0: #Modifikator ist 0
                                    await send(f'Nun {person} leider ist dies ein **kritischer Fehlschlag** doch bleiben Sie standhaft. Noch ist nichts verloren.\nErgebnis: **{result}** [||{rolls_str}||]')
                                else:
                                    await send(f'Nun {person} leider ist dies ein **kritischer Fehlschlag** doch bleiben Sie standhaft. Noch ist nichts verloren.\nErgebnis: **{result}** [||{rolls_str} - {j}||]')
                            elif 20 in rolls:
                                if j == 0: #Modifikator ist 0
                                    await send(f'"Meinen Glückwunsch für Ihren **kritischen Erfolg** {person}. Ich hoffe mit diesem Wurf kommen Sie weiter.\nErgebnis: **{result}** [||{rolls_str}||]')
                                else:
                                    await send(f'"Meinen Glückwunsch für Ihren **kritischen Erfolg** {person}. Ich hoffe mit diesem Wurf kommen Sie weiter.\nErgebnis: **{result}** [||{rolls_str} - {j}||]')
                            else:
                                if j == 0: #Modifikator ist 0
                                    await send(f'{person} Ergebnis: **{result}** [||{rolls_str}||]')
                                else:
                                    await send(f'{person} Ergebnis: **{result}** [||{rolls_str} - {j}||]')
                        else:
                            if j == 0:
                                await send(f'{person} Ergebnis: **{result}** [||{rolls_str}||]')
                            else:
                                await send(f'{person} Ergebnis: **{result}** [||{rolls_str} - {j}||]')
                    else:
                        if j == 0:
                            await send(f'{person} Ergebnis: **{result}** [||{rolls_str}||]')
                        else:
                            await send(f'{person} Ergebnis: **{result}** [||{rolls_str} - {j}||]')
                else:
                    if n == 1:
                        if i == 20:
                            if 1 in rolls:
                                if j == 0: #Modifikator ist 0
                                    await send(f'Nun {person} leider ist dies ein **kritischer Fehlschlag** doch bleiben Sie standhaft. Noch ist nichts verloren.\nErgebnis: **{result}** [{rolls_str}]')
                                else:
                                    await send(f'Nun {person} leider ist dies ein **kritischer Fehlschlag** doch bleiben Sie standhaft. Noch ist nichts verloren.\nErgebnis: **{result}** [||{rolls_str} + {j}||]')
                            elif 20 in rolls:
                                if j == 0:
                                    await send(f'"Meinen Glückwunsch für Ihren **kritischen Erfolg** {person}. Ich hoffe mit diesem Wurf kommen Sie weiter.\nErgebnis: **{result}** [||{rolls_str} + {j}||]')
                                else:
                                    await send(f'"Meinen Glückwunsch für Ihren **kritischen Erfolg** {person}. Ich hoffe mit diesem Wurf kommen Sie weiter.\nErgebnis: **{result}** [||{rolls_str} + {j}||]')
                            else:
                                if j == 0: #Modifikator ist 0
                                    await send(f'{person} Ergebnis: **{result}** [||{rolls_str}||]')
                                else:
                                    await send(f'{person} Ergebnis: **{result}** [||{rolls_str} + {j}||]')
                        else:
                            if j == 0: #Modifikator ist 0
                                await send(f'{person} Ergebnis: **{result}** [||{rolls_str}||]')
                            else:
                                await send(f'{person} Ergebnis: **{result}** [||{rolls_str} + {j}||]')
                    else:
                        if j == 0: #Modifikator ist 0
                            await send(f'{person} Ergebnis: **{result}** [||{rolls_str}||]')
                        else:
                            await send(f'{person} Ergebnis: **{result}** [||{rolls_str} + {j}||]')
        else:
            await send(f'{person}, bitte gib einen gültigen Befehl ein, z.B. "/roll 2d6+3 Feuerschaden" oder "/roll 1d20+5"')
    
    #Vorteil
    elif message.content.startswith('/Vorteil') or message.content.startswith('/vorteil'):
        command = message.content[9:].strip().lower()  # command = "i"
        i = 0
        if '+' in command:
            parts = command.split('+', 1)
            command = parts[0].strip()
            modifier = parts[1].strip()
            if modifier.isdigit():
                i = int(modifier)
        else:
            i = int(command) if command else 0
        rolls = [random.randint(1, 20) for _ in range(2)]
        result = max(rolls) + i
        rolls_str = ", ".join(map(str, rolls))

        if i > 0:
            if max(rolls) == 1:  # Doppel 1
                await send(f"Ich hoffe der Wurf war nicht wichtig {person} \nErgebnis: **{result}** (||{max(rolls)} + {i}||) [||{rolls_str}||]")
            elif max(rolls) == 20:  # Irgendeine Natürliche 20
                await send(f"Meinen Glückwunsch für Ihren kritischen Erfolg {person}. Ich hoffe mit diesem Wurf kommen Sie weiter.\nErgebnis: **{result}** (||{max(rolls)} + {i}||) [||{rolls_str}||]")
            else:  # Irgendein Wurf
                await send(f"{person}: Ergebnis: **{result}** (||{max(rolls)} + {i}||) [||{rolls_str}||]")
        elif i < 0:
            i = abs(i)
            if max(rolls) == 1:  # Doppel 1
                await send(f"Ich hoffe der Wurf war nicht wichtig {person} \nErgebnis: **{result}** (||{max(rolls)} - {i}||) [{rolls_str}]")
            elif max(rolls) == 20:  # Irgendeine Natürliche 20
                await send(f"Meinen Glückwunsch für Ihren kritischen Erfolg {person}. Ich hoffe mit diesem Wurf kommen Sie weiter.\nErgebnis: **{result}** (||{max(rolls)} - {i}||) [||{rolls_str}||]")
            else:  # Irgendein Wurf
                await send(f"{person}: Ergebnis: **{result}** (||{max(rolls)} - {i}||) [||{rolls_str}||]")
        elif i == 0:
            if max(rolls) == 1:  # Doppel 1
                await send(f"Ich hoffe der Wurf war nicht wichtig {person} \nErgebnis: **{result}** (||{max(rolls)}||) [||{rolls_str}||]")
            elif max(rolls) == 20:  # Irgendeine Natürliche 20
                await send(f"Meinen Glückwunsch für Ihren kritischen Erfolg {person}. Ich hoffe mit diesem Wurf kommen Sie weiter.\nErgebnis: **{result}** (||{max(rolls)}||) [||{rolls_str}||]")
            else:  # Irgendein Wurf
                await send(f"{person}: Ergebnis: **{result}** (||{max(rolls)}||) [||{rolls_str}||]")

    #Nachteil
    elif message.content.startswith('/Nachteil') or message.content.startswith('/nachteil'):
        command = message.content[10:].strip().lower()  # command = "i"
        i = 0
        if '+' in command:
            parts = command.split('+', 1)
            command = parts[0].strip()
            modifier = parts[1].strip()
            if modifier.isdigit():
                i = int(modifier)
        else:
            i = int(command) if command else 0

        rolls = [random.randint(1, 20) for _ in range(2)]
        result = min(rolls) + i
        rolls_str = ", ".join(map(str, rolls))

        if i > 0:
            if min(rolls) == 1:  # Eine 1 wurde geworfen
                await send(f'Das Glück ist Ihnen heute aber nicht hold, {person}\nErgebnis: **{result}** (||{min(rolls)} + {i}||) [||{rolls_str}||]')
            elif min(rolls) == 20:  # Doppel 20
                await send(f'Ich glaube, ich traue meinen Augen gerade nicht, aber Sie, {person}, haben gerade einen doppelten kritischen Erfolg erzielt. Chapeau! \nErgebnis: **{result}** (||{min(rolls)} + {i}||) [||{rolls_str}||]')
            else:  # Irgendein Wurf
                await send(f"{person}: Ergebnis: **{result}** (||{min(rolls)} + {i}||) [||{rolls_str}||]")
        elif i < 0:
            i = abs(i)
            if min(rolls) == 1:  # Eine 1 wurde geworfen
                await send(f'Das Glück ist Ihnen heute aber nicht hold, {person}\nErgebnis: **{result}** (||{min(rolls)} - {i}||) [||{rolls_str}||]')
            elif min(rolls) == 20:  # Doppel 20
                await send(f'Ich glaube, ich traue meinen Augen gerade nicht, aber Sie, {person}, haben gerade einen doppelten kritischen Erfolg erzielt. Chapeau! \nErgebnis: **{result}** ({min(rolls)} - {i}) [||{rolls_str}||]')
            else:  # Irgendein Wurf
                await send(f"{person}: Ergebnis: **{result}** (||{min(rolls)} - {i}||) [||{rolls_str}||]")
        elif i == 0:
            if min(rolls) == 1:  # Eine 1 wurde geworfen
                await send(f'Das Glück ist Ihnen heute aber nicht hold, {person}\nErgebnis: **{result}** (||{min(rolls)}||) [||{rolls_str}||]')
            elif min(rolls) == 20:  # Doppel 20
                await send(f'Ich glaube, ich traue meinen Augen gerade nicht, aber Sie, {person}, haben gerade einen doppelten kritischen Erfolg erzielt. Chapeau! \nErgebnis: **{result}** ({min(rolls)}) [||{rolls_str}||]')
            else:  # Irgendein Wurf
                await send(f"{person}: Ergebnis: **{result}** (||{min(rolls)}||) [||{rolls_str}||]")
    

    #Attribute
    elif c == '/attribute':
        attributes = []
        ergebnis = 0
        for i in range(1, 7):
            rolls = sorted([random.randint(1, 6) for _ in range(4)])[0:]
            total = sum(rolls) - rolls[0]
            low = rolls[0]
            rolls[0]= "~~" + str(low) + "~~"
            attributes.append((rolls, total))
            ergebnis = ergebnis + total
        response = '\n'.join([f'Wert {i}: {rolls}. (**{total}**)' for i, (rolls, total) in enumerate(attributes, start=1)])

        await send(response + '\n'+ "Total = **" + str(ergebnis)+"**")
        
    #Fertigkeiten
    elif c.startswith('/initiative') or c.startswith('/ini') or c.startswith('/akrobatik') or c.startswith('/acrobatics') or c.startswith('/athletik') or c.startswith('/athletics') or c.startswith('/arkane') or c.startswith('/arcana') or c.startswith('/akrobatik') or c.startswith('/tier') or c.startswith('/animal') or c.startswith('/täuschen') or c.startswith('/deception') or c.startswith('/geschichte') or c.startswith('/history') or c.startswith('/motiv') or c.startswith('/insight') or c.startswith('/einschüchtern') or c.startswith('/intimidation') or c.startswith('/nachforschen') or c.startswith('/investigation') or c.startswith('/heilkunde') or c.startswith('/medicine')  or c.startswith('/naturkunde') or c.startswith('/nature') or c.startswith('/wahrnehmung') or c.startswith('/perception') or c.startswith('/auftreten') or c.startswith('/performance') or c.startswith('/überzeugen') or c.startswith('/persuasion') or c.startswith('/religion') or c.startswith('/fingerfertigkeit') or c.startswith('/finger') or c.startswith('/heimlichkeit') or c.startswith('/stealth') or c.startswith('/überleben') or c.startswith('/survival') or c.startswith('/str') or c.startswith('/dex') or c.startswith('/ges') or c.startswith('/kon') or c.startswith('/int') or c.startswith('/wis') or c.startswith('/cha') or c.startswith('/strength') or c.startswith('/intelligence') or c.startswith('/konstitution') or c.startswith('/weisheit') or c.startswith('/charisma') or c.startswith('/strength') or c.startswith('/stärke') or c.startswith('/intelligence') or c.startswith('/intelligenz') or c.startswith('/dexterity') or c.startswith('/geschklichkeit') or c.startswith('/wisdom') or c.startswith('/nachforschung') or c.startswith('/con') or c.startswith('/alchemist') or c.startswith('/thieves') or c.startswith('/dieb') or c.startswith('/kaligraphie') or c.startswith('/schmied') or c.startswith('/koch') or c.startswith('/cooking') or c.startswith('/tinker') or c.startswith('/tüftler') or c.startswith('/navigator') or c.startswith('/vehicles') or c.startswith('/konsti') or c.startswith('/herbalism') or c.startswith('/heilkräuter'):
        command = message.content[1:].strip()  # Initialisiere die Variable 'command'

        if '+' in command:
            parts = command.split('+', 1)
            command = parts[0].strip()
            modifier_str = parts[1].strip()
            if modifier_str.isdigit():
                modifier = int(modifier_str)
        elif '-' in command:
            parts = command.split('-', 1)
            command = parts[0].strip()
            modifier_str = parts[1].strip()
            if modifier_str.isdigit():
                modifier = -int(modifier_str)
        else:
            modifier = 0

        parts = command.split(' ')
        skill = parts[0].strip().lower()
        skills = ['str','stärke','strength','ges','geschicklichkeit','dex','dexterity','kon', 'con','konstitution','int','intelligence','intelligenz','wis','wisdom','weisheit','wei','charisma','cha','initiative', 'ini', 'akrobatik', 'acrobatics', 'athletik', 'athletics', 'arkana', 'arcana', 'tier', 'animal', 'täuschen', 'deception', 'geschichte', 'history', 'motiv', 'insight', 'einschüchtern', 'intimidation', 'nachforschen', 'investigation', 'heilkunde', 'medicine', 'naturkunde', 'nature', 'wahrnehmung', 'perception', 'auftreten', 'performance', 'überzeugen', 'persuasion', 'religion', 'fingerfertigkeit', 'finger', 'heimlichkeit', 'stealth', 'überleben', 'survival', 'arkane', 'nachforschung', 'alchemist', 'thieves', 'dieb', 'kaligraphie', 'schmied', 'smith', 'koch', 'cooking', 'tinker', 'tüftler', 'navigator', 'vehicles', 'initiative', 'konsti','heilkräuter','herbalism']

        if skill == 'tier':
            skill_name = 'mit Tieren umgehen'
        elif skill == 'alchemist':
            skill_name = 'Alchemisten Ausrüstung'
        elif skill == 'heilkräuter':
            skill_name = 'Heilkräuter Ausrüstung'
        elif skill == 'herbalism':
            skill_name = 'Herbalismkit'
        elif skill == 'thieves':
            skill_name = 'Thieves Tools'
        elif skill == 'navigator':
            skill_name = 'Navigator Ausrüstung'
        elif skill == 'vehicles':
            skill_name = 'Vehicles'
        elif skill == 'dieb':
            skill_name = 'Diebeswerkzeug'
        elif skill == 'kaligraphie':
            skill_name = 'Kaligraphie Ausrüstung'
        elif skill == 'schmied':
            skill_name = 'Schmiede Werkzeuge'
        elif skill == 'smith':
            skill_name = 'Smith Tools'
        elif skill == 'koch':
            skill_name = 'Kochuntersilien'    
        elif skill == 'cooking':
            skill_name = 'Cooking Tools'
        elif skill == 'tinker':
            skill_name = 'Tinker Tools'
        elif skill == 'tüftler':
            skill_name = 'Tüftler Werkzeuge'
        elif skill == 'animal':
            skill_name = 'Animal Handling'
        elif skill == 'arkane':
            skill_name = 'Arkane Kunde'
        elif skill == 'motiv':
            skill_name = 'Motiv erkennen'
        elif skill == 'finger':
            skill_name = 'Sleight of Hand'
        elif skill == 'str':
            skill_name = 'Stärke'
        elif skill == 'ges':
            skill_name = 'Geschicklichkeit'
        elif skill == 'dex':
            skill_name = 'Dexterity'
        elif skill == 'con':
            skill_name = 'Constitution'
        elif skill == 'kon':
            skill_name = 'Konstitution'
        elif skill == 'konsti':
            skill_name = 'Konstitution'
        elif skill == 'int':
            skill_name = 'Intelligenz'
        elif skill == 'wis':
            skill_name = 'Wisdom'
        elif skill == 'cha':
            skill_name = 'Charisma'
        elif skill == 'ini':
            skill_name = 'Initiative'
        elif skill in skills:
            skill_name = skill.capitalize()
        else:
            skill_name = skill

        if skill in skills or skill == 'initiative':
            roll = random.randint(1, 20)
            result = roll + modifier if modifier > 0 else roll - abs(modifier)
            if roll == 1:
                await send(f'Nun {person}, leider haben Sie einen kritischen Fehlschlag. Verzagen Sie nicht, es gibt immer andere Möglichkeiten.\n_**{skill_name}:**_ **{result}** [||{roll} {"+" if modifier > 0 else "-"} {abs(modifier)}||]')
            elif roll == 20:
                await send(f'Mein Glückwunsch {person}, Sie sind wohl sehr gut in dem, was Sie gerade machen. Beschreiben Sie, wie das aussieht, wenn es Ihnen gefällt.\n_**{skill_name}**_ **{result}** [||{roll} {"+" if modifier >= 0 else "-"} {abs(modifier)}||]')
            else:
                await send(f'{person}\n_**{skill_name}:**_ **{result}** [||{roll} {"+" if modifier >= 0 else "-"} {abs(modifier)}||]')
        else:
            await send(f'{person}, gib bitte einen gültigen Befehl ein, wie z.B. **/Charisma +5**.')
    #Waffen
    elif c.startswith('/longsword') or c.startswith('/club') or c.startswith('/dagger') or c.startswith('/greatclub') or c.startswith('/handaxe') or c.startswith('/javelin') or c.startswith('/hammer') or c.startswith('/mace') or c.startswith('/quarterstaff') or c.startswith('/sickle') or c.startswith('/spear') or c.startswith('/crossbow') or c.startswith('/dart') or c.startswith('/shortbow') or c.startswith('/sling') or c.startswith('/battleaxe') or c.startswith('/flail') or c.startswith('/glaive') or c.startswith('/greataxe') or c.startswith('/greatsword') or c.startswith('/halberd') or c.startswith('/lance') or c.startswith('/maul') or c.startswith('/morningstar') or c.startswith('/pike') or c.startswith('/rapier') or c.startswith('/scimitar') or c.startswith('/shortsword') or c.startswith('/trident') or c.startswith('/warhammer') or c.startswith('/whip') or c.startswith('/blowgun') or c.startswith('/handcrossbow') or c.startswith('/heavycrossbow') or c.startswith('/longbow') or c.startswith('/net') or c.startswith('/beil') or c.startswith('/dolch') or c.startswith('/kampfstab') or c.startswith('/knüppel') or c.startswith('/sichel') or c.startswith('/speer') or c.startswith('/streitkolben') or c.startswith('/wurfspeer') or c.startswith('/GroßerKnüppel') or c.startswith('/armbrust') or c.startswith('/kurzbogen') or c.startswith('/schleuder') or c.startswith('/dreizack') or c.startswith('/flegel') or c.startswith('/gleve') or c.startswith('/großschwert') or c.startswith('/hellebarde') or c.startswith('/kriegshacke') or c.startswith('/kriegshammer') or c.startswith('/krummsäbel') or c.startswith('/säbel') or c.startswith('/kurzschwert') or c.startswith('/langschwert') or c.startswith('/lanze') or c.startswith('/morgenstern') or c.startswith('/peitsche') or c.startswith('/streitaxt') or c.startswith('/zweihandaxt') or c.startswith('/zweihandhammer') or c.startswith('/zweihandschwert') or c.startswith('/handarmbrust') or c.startswith('/schwerearmbrust') or c.startswith('/blasrohr') or c.startswith('/langbogen') or c.startswith('/netz') or c.startswith('/katana') or c.startswith('/unarmed') or c.startswith('/waffenlos'):
        command = message.content[1:].strip()  # Initialisiere die Variable 'command'

        if '+' in command:
            parts = command.split('+', 1)
            command = parts[0].strip()
            modifier_str = parts[1].strip()
            if modifier_str.isdigit():
                modifier = int(modifier_str)
        elif '-' in command:
            parts = command.split('-', 1)
            command = parts[0].strip()
            modifier_str = parts[1].strip()
            if modifier_str.isdigit():
                modifier = -int(modifier_str)
        else:
            modifier = 0

        parts = command.split(' ')
        waffe = parts[0].strip().lower() 
        weapons = ['unarmed','waffenlos','longsword', 'club', 'dagger', 'greatclub', 'handaxe', 'javelin', 'hammer', 'mace', 'quarterstaff', 'sickle', 'spear', 'crossbow', 'dart', 'shortbow', 'sling', 'battleaxe', 'flail', 'glaive', 'greataxe', 'greatsword', 'halberd', 'lance', 'maul', 'morningstar', 'pike', 'rapier', 'scimitar', 'shortsword', 'trident', 'warhammer', 'whip', 'blowgun', 'handcrossbow', 'heavycrossbow', 'longbow', 'net', 'beil', 'dolch', 'kampfstab', 'knüppel', 'sichel', 'speer', 'streitkolben', 'wurfspeer', 'GroßerKnüppel', 'armbrust', 'kurzbogen', 'schleuder', 'dreizack', 'flegel', 'gleve', 'hellebarde', 'kriegshacke', 'kriegshammer', 'krummsäbel', 'säbel', 'kurzschwert', 'langschwert', 'lanze', 'morgenstern', 'peitsche', 'streitaxt', 'zweihandaxt', 'zweihandhammer', 'zweihandschwert', 'handarmbrust', 'schwerearmbrust', 'blasrohr', 'langbogen', 'netz', 'katana']

        if waffe.lower() == 'crossbow':
            waffe_formatted = 'Light Crosbow'
        elif waffe.lower() == 'armbrust':
            waffe_formatted = 'Leichte Armbrust'
        elif waffe.lower() == 'handcrossbow':
            waffe_formatted = 'Hand Crossbow'
        elif waffe.lower() == 'heavycrossbow':
            waffe_formatted = 'Heavy Crossbow'
        elif waffe.lower() == 'schwerearmbrust':
            waffe_formatted = 'Schwere Armbrust'
        elif waffe.lower() == 'unarmed':
            waffe_formatted = 'Unarmed Strike'
        elif waffe.lower() == 'waffenlos':
            waffe_formatted = 'Waffenloser Angriff'
        else:
            waffe_formatted = waffe.capitalize()
        
        if waffe in weapons:
            roll = random.randint(1, 20)
            result = roll + modifier if modifier > 0 else roll - abs(modifier)
            if roll == 1:
                await send(f'Nun {person}, leider haben Sie einen kritischen Fehlschlag. Verzagen Sie nicht, es gibt immer andere Möglichkeiten.\n_**{waffe_formatted}:**_ **{result}** [||{roll} {"+" if modifier >= 0 else "-"} {abs(modifier)}||]')
            elif roll == 20:
                await send(f'Mein Glückwunsch {person}, Sie sind wohl sehr gut in dem, was Sie gerade machen. Beschreiben Sie, wie das aussieht, wenn es Ihnen gefällt.\n_**{waffe_formatted}**_ **{result}** [||{roll} {"+" if modifier >= 0 else "-"} {abs(modifier)}||]')
            else:
                await send(f'{person}\n_**{waffe_formatted}:**_ **{result}** [||{roll} {"+" if modifier >= 0 else "-"} {abs(modifier)}||]')
        else:
            await send(f'{person}, gib bitte einen gültigen Befehl ein, wie z.B. **/Waffenlos +5**.')
    
client.run(token)  

#Link: https://discord.com/oauth2/authorize?client_id=1276233268244517038&permissions=580997674773568&integration_type=0&scope=bot