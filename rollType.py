import commandsHandler

ATTRIBUTE = {
    "str": "Strength",
    "stärke": "Strength",
    "strength": "Strength",
    "ges": "Dexterity",
    "geschicklichkeit": "Dexterity",
    "dex": "Dexterity",
    "dexterity": "Dexterity",
    "kon": "Constitution",
    "con": "Constitution",
    "konstitution": "Constitution",
    "constitution": "Constitution",
    "konsti": "Constitution",
    "int": "Intelligenz",
    "intelligence": "Intelligenz",
    "intelligenz": "Intelligenz",
    "wis": "Wisdom",
    "wisdom": "Wisdom",
    "weisheit": "Wisdom",
    "wei": "Wisdom",
    "charisma": "Charisma",
    "cha": "Charisma",
}

SKILL = {
    "initiative": "Initiative",
    "ini": "Initiative",
    "init": "Initiative",
    "akrobatik": "Acrobatics",
    "acrobatics": "Acrobatics",
    "tier": "Animal Handling",
    "animal": "Animal Handling",
    "animalhandling": "Animal Handling",
    "arkana": "Arcana",
    "arcana": "Arcana",
    "athletik": "Athletics",
    "athletics": "Athletics",
    "täuschen": "Deception",
    "deception": "Deception",
    "geschichte": "History",
    "history": "History",
    "motiv": "Insight",
    "insight": "Insight",
    "einschüchtern": "Intimidation",
    "intimidation": "Intimidation",
    "nachforschen": "Investigation",
    "nachforschung": "Investigation",
    "investigation": "Investigation",
    "heilkunde": "Medicine",
    "medicine": "Medicine",
    "naturkunde": "Nature",
    "nature": "Nature",
    "wahrnehmung": "Perception",
    "perception": "Perception",
    "auftreten": "Performance",
    "performance": "Performance",
    "überzeugen": "Persuasion",
    "persuasion": "Persuasion",
    "religion": "Religion",
    "fingerfertigkeit": "Sleight of Hand",
    "finger": "Sleight of Hand",
    "sleight": "Sleight of Hand",
    "heimlichkeit": "Stealth",
    "stealth": "Stealth",
    "überleben": "Survival",
    "survival": "Survival",
}

PROFICIENCY = {
    "alchemist": "Alchemistkit",
    "alchemy": "Alchemistkit",
    "thieves": "Thieves Cant",
    "dieb": "Thieves Cant",
    "kaligraphie": "Calygraphykit",
    "calycraphy": "Calygraphykit",
    "schmied": "Smithing Tools",
    "smith": "Smithing Tools",
    "koch": "Cooking Tools",
    "cooking": "Cooking Tools",
    "tinker": "Tinker Tools",
    "tüftler": "Tinker Tools",
    "navigator": "Navigator",
    "vehicles": "Vehicles",
    "heilkräuter": "Herbalismkit",
    "herbalism": "Herbalismkit",
}


def addSkillRolls(bot):
    for input, skill_name in SKILL.items():
        @bot.command(name=input, skill_name=skill_name)
        async def skill(ctx, *args):
            extra = " ".join(args)
            user = ctx.author
            await ctx.send(commandsHandler.skillRoll(skill_name, extra, user))


def addAttributeRolls(bot):
    for input, attribute_name in ATTRIBUTE.items():
        @bot.command(name=input)
        async def attribute(ctx, *args, attribute_name=attribute_name):
            extra = " ".join(args)
            user = ctx.author
            await ctx.send(commandsHandler.skillRoll(attribute_name, extra, user))


def addProficiencyRolls(bot):
    for input, proficiency_name in PROFICIENCY.items():
        @bot.command(name=input)
        async def proficiency(ctx, *args, proficiency_name=proficiency_name):
            extra = " ".join(args)
            user = ctx.author
            await ctx.send(commandsHandler.skillRoll(proficiency_name, extra, user))