import importlib

from Hack import bot, botname
from logger import LOGGER
from Hack.plugins import ALL_MODULES


async def initiate_bot():
    LOGGER(__name__).info('IMPORTING MODULES')
    for all_module in ALL_MODULES:
        importlib.import_module("Hack.plugins." + all_module)
    LOGGER(__name__).info('MODULES IMPORTED SUCCESSFULLY')
    await bot.run_until_disconnected()


if __name__ == '__main__':
    bot.loop.run_until_complete(initiate_bot())
    LOGGER(__name__).info(f'{botname} IS STOPPED')
