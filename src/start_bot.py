import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.config import getSettings
from bot.telegramBot import runBot


class MinimalApp:
    def __init__(self, settings):
        self.settings = settings
        self.title = settings.APP_NAME 
    pass

settings = getSettings()
app = MinimalApp(settings)

async def main():
    print("Starting Telegram Bot in standalone mode...")
    await runBot(app)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Telegram Bot stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.config import getSettings
from bot.telegramBot import runBot


class MinimalApp:
    def __init__(self, settings):
        self.settings = settings
        self.title = settings.APP_NAME 
    pass

settings = getSettings()
app = MinimalApp(settings)

async def main():
    print("Starting Telegram Bot in standalone mode...")
    await runBot(app)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Telegram Bot stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
