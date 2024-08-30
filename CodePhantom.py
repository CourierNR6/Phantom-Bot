from dotenv import load_dotenv
import os

import discord
from discord.ext import commands

import slashCommands
import rollType, weaponType
import chaosRolls
import easterEggs

load_dotenv()
token = os.environ["TOKEN"]

bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()

slashCommands.rollCommand(bot)
slashCommands.vorteilCommand(bot)
slashCommands.nachteilCommand(bot)
slashCommands.attributeCommand(bot)
rollType.addSkillRolls(bot)
rollType.addAttributeRolls(bot)
rollType.addProficiencyRolls(bot)
weaponType.addWeaponRolls(bot)
chaosRolls.chaos(bot)
easterEggs.hideEasterEggs(bot)


bot.run(token)  

#Link: https://discord.com/oauth2/authorize?client_id=1276233268244517038&permissions=580997674773568&integration_type=0&scope=bot