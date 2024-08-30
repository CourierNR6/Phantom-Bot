from dotenv import load_dotenv
import os
import discord
import random
import re
from discord.ext import commands
from discord import app_commands
import commandsHandler

import weaponType
import rollType

load_dotenv()
token = os.environ["TOKEN"]

bot = commands.Bot(command_prefix="/",intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()


weaponType.addWeaponRolls(bot)
rollType.addSkillRolls(bot)
rollType.addAttributeRolls(bot)
rollType.addProficiencyRolls(bot)

@bot.tree.command(name="roll",description="Roll dice")
@app_commands.rename(roll_text="roll")
@app_commands.describe(roll_text='ex: 1d20+12 fire', modifier='overwrites mod in text', damage='overwrites dmg in text')
async def roll(interaction:discord.Interaction, roll_text: str, modifier: int=0, damage: str=""):
    await interaction.response.send_message(commandsHandler.roll(interaction.user, roll_text, modifier, damage))

@bot.tree.command(name="vorteil",description="Roll with advantage")
async def vorteil(interaction:discord.Interaction, modifier: int=0):
    await interaction.response.send_message(commandsHandler.vorteil(interaction.user, modifier))

@bot.tree.command(name="nachteil",description="Roll with disadvantage")
async def nachteil(interaction:discord.Interaction, modifier: int=0):
    await interaction.response.send_message(commandsHandler.nachteil(interaction.user, modifier))

@bot.tree.command(name="attribute",description="Roll for your attributes")
async def attribute(interaction:discord.Interaction):
    await interaction.response.send_message(commandsHandler.attribute())

bot.run(token)  

#Link: https://discord.com/oauth2/authorize?client_id=1276233268244517038&permissions=580997674773568&integration_type=0&scope=bot