import discord
from discord import app_commands
from discord.ext import commands
import logging
from logging.handlers import SysLogHandler
from handlers import handle_rating_command
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger('discord_bot')
logger.setLevel(logging.INFO)
handler = SysLogHandler(address='/dev/log')
formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Get token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("No token found in environment variables")

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        print("Syncing commands...")
        try:
            await self.tree.sync()
            print("Command tree synced globally")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')

@bot.tree.command()
@app_commands.describe(name="The name to look up ratings for")
async def rating(interaction: discord.Interaction, name: str):
    """Gets rating information for the given name."""

    user = f"{interaction.user.name}#{interaction.user.discriminator}"
    channel = f"#{interaction.channel.name}" if hasattr(interaction.channel, 'name') else "DM"
    server = interaction.guild.name if interaction.guild else "DM"

    response = await handle_rating_command(user, channel, server, name)
    await interaction.response.send_message(response)

bot.run(TOKEN)