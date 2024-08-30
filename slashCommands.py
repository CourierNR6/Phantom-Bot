import discord
from discord import app_commands
import commandsHandler

def rollCommand(bot):
    @bot.tree.command(name="roll",description="Roll dice")
    @app_commands.rename(roll_text="roll")
    @app_commands.describe(roll_text='ex: 1d20+12 fire', modifier='overwrites mod in text', damage='overwrites dmg in text')
    async def roll(interaction:discord.Interaction, roll_text: str, modifier: int=0, damage: str=""):
        await interaction.response.send_message(commandsHandler.roll(interaction.user, roll_text, modifier, damage))

def vorteilCommand(bot):
    @bot.tree.command(name="vorteil",description="Roll with advantage")
    async def vorteil(interaction:discord.Interaction, modifier: int=0):
        await interaction.response.send_message(commandsHandler.vorteil(interaction.user, modifier))

def nachteilCommand(bot):
    @bot.tree.command(name="nachteil",description="Roll with disadvantage")
    async def nachteil(interaction:discord.Interaction, modifier: int=0):
        await interaction.response.send_message(commandsHandler.nachteil(interaction.user, modifier))

def attributeCommand(bot):
    @bot.tree.command(name="attribute",description="Roll for your attributes")
    async def attribute(interaction:discord.Interaction):
        await interaction.response.send_message(commandsHandler.attribute())
