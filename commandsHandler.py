
import random
import re

import damageType


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