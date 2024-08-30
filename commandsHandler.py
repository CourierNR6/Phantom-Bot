
import random
import re

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