from dotenv import load_dotenv
import os

import discord
from discord.ext import commands

from botCommands import slashCommands, promptCommands

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
promptCommands.addSkillRolls(bot)
promptCommands.addAttributeRolls(bot)
promptCommands.addProficiencyRolls(bot)
promptCommands.addWeaponRolls(bot)
promptCommands.chaos(bot)
promptCommands.hideEasterEggs(bot, commands)


bot.run(token)  

#Link: https://discord.com/oauth2/authorize?client_id=1276233268244517038&permissions=580997674773568&integration_type=0&scope=bot
