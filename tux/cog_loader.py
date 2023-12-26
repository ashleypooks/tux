from discord.ext import commands
import os
from utils._tux_logger import TuxLogger
import logging
import traceback

logger = TuxLogger(__name__)


class CogLoader(commands.Cog):
    def __init__(self, bot, debug=False):
        """
        Constructor for the CogLoader Cog.

        Parameters:
            bot (commands.Bot): The instance of the Discord bot.
            debug (bool): A flag indicating whether debug mode is enabled.
        """
        self.bot = bot
        self.debug = debug
        self.ignore_cogs = []
        if debug:
            logger.setLevel(logging.DEBUG)

    async def _load_cogs_from_folder(self, folder_name):
        """
        Dynamically loads cogs from the specified subdirectory.

        Each cog module should be a Python file in the specified directory.
        The file name (excluding extension) is considered the cog name.
        """
        cog_dir = os.path.join(os.path.dirname(__file__), folder_name)

        for filename in os.listdir(cog_dir):
            cog_name = filename[:-3]
            module = f'{folder_name}.{cog_name}'

            if not filename.endswith('.py') or\
                    cog_name in self.ignore_cogs or\
                    filename.startswith('_'):
                logger.info(f"Skipping {module}.", __name__)
                continue

            try:
                await self.bot.load_extension(module)
                logger.debug(f'Successfully loaded cog: {module}', __name__)
            except Exception as e:
                logger.error(f'Failed to load cog {module}. Error: {e}', __name__)
                logger.error(traceback.format_exc())

    async def load_events(self):
        """Load cogs from the 'events' folder."""
        await self._load_cogs_from_folder('events')

    async def load_utils(self):
        """Load cogs from the 'utils' folder."""
        await self._load_cogs_from_folder('utils')

    async def load_commands(self):
        """Load cogs from the 'commands' folder."""
        await self._load_cogs_from_folder('commands')

    @classmethod
    async def setup(cls, bot, debug=False):
        """
        Sets up the CogLoader Cog and adds it to the bot.

        Parameters:
            bot (commands.Bot): The instance of the Discord bot.
            debug (bool): A flag indicating whether debug mode is enabled.
        """
        cog = cls(bot, debug)
        await cog.load_events()
        await cog.load_utils()
        await cog.load_commands()
        await bot.add_cog(cog)
