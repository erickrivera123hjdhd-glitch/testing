import os
import sys
import logging

# Allow imports like `from src...` when Wispbyte runs `python3 src/main.py`.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
from src.config import Config
from src.commands.setup import setup_command
from src.commands.panel import panel_command
from src.commands.status import status_command
from src.commands.bridge import bridge_command
from src.commands.permissions import permissions_command
from src.commands.disconnect import disconnect_command
from src.commands.help import help_command
from src.bridge.server import BridgeServer
from src.database.database import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobloxControlBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix='/', intents=intents, description='Roblox Remote Control Dashboard')
        self.config = Config()
        self.db = Database()
        self.bridge_server = None

        self.tree.add_command(setup_command)
        self.tree.add_command(panel_command)
        self.tree.add_command(status_command)
        self.tree.add_command(bridge_command)
        self.tree.add_command(permissions_command)
        self.tree.add_command(disconnect_command)
        self.tree.add_command(help_command)

    async def setup_hook(self):
        await self.tree.sync()
        logger.info('Commands synced')
        if self.config.bridge_host and self.config.bridge_port:
            self.bridge_server = BridgeServer(self.config, self.db)
            await self.bridge_server.start()
            logger.info('Bridge server started')


bot = RobloxControlBot()


@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')


if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise RuntimeError('DISCORD_TOKEN is not set')
    bot.run(token)
