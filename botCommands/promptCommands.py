import random
import handlers.commandsHandler as commandsHandler
from customTypes.chaosRolls import CHAOS
from customTypes.easterEggs import EASTEREGG
from customTypes.rollType import SKILL, ATTRIBUTE, PROFICIENCY
from customTypes.weaponType import WEAPON

def addWeaponRolls(bot):
    for weapon_input, weapon_name in WEAPON.items():
        @bot.command(name=weapon_input)
        async def weapon(ctx, *args, weapon_name=weapon_name):
            extra = " ".join(args)
            user = ctx.author
            await ctx.send(commandsHandler.weaponRoll(weapon_name, extra, user))


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

def hideEasterEggs(bot, commands):
    for egg_name, egg_message in EASTEREGG.items():
        # Create a command handler for each egg_name
        command = commandsHandler.create_dynamic_dic_command(egg_name, egg_message)
        bot.add_command(commands.Command(command, name=egg_name))


def chaos(bot):
    @bot.command()
    async def chaos(ctx):
        result = random.randint(1, 100)
        answer = CHAOS[result]
        user = ctx.author
        mention = user.mention
        send_text = f'||{result}|| {mention}, you disturbed the order of the weaves of magic:\n> {answer}'
        await ctx.send(send_text)
