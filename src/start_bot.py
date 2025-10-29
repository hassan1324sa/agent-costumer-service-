import asyncio
import sys
import os

# Add the parent directory to the path to allow imports from src/helpers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.config import getSettings
from bot.telegramBot import runBot

# Create a minimal object to simulate the 'app' object needed by runBot
# This assumes runBot only uses app.settings and app.title
class MinimalApp:
    def __init__(self, settings):
        self.settings = settings
        self.title = settings.APP_NAME 
    pass

# Initialize the minimal app object with settings
settings = getSettings()
app = MinimalApp(settings)

# The runBot function is async, so we need an asyncio loop to run it
async def main():
    print("Starting Telegram Bot in standalone mode...")
    # runBot uses polling (updater.start_polling()), which is suitable for standalone operation
    await runBot(app)

if __name__ == "__main__":
    try:
        # The runBot function uses async, so we use asyncio.run
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Telegram Bot stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
import asyncio
import sys
import os

# Add the parent directory to the path to allow imports from src/helpers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.config import getSettings
from bot.telegramBot import runBot

# Create a minimal object to simulate the 'app' object needed by runBot
# This assumes runBot only uses app.settings and app.title
class MinimalApp:
    def __init__(self, settings):
        self.settings = settings
        self.title = settings.APP_NAME 
    pass

# Initialize the minimal app object with settings
settings = getSettings()
app = MinimalApp(settings)

# The runBot function is async, so we need an asyncio loop to run it
async def main():
    print("Starting Telegram Bot in standalone mode...")
    # runBot uses polling (updater.start_polling()), which is suitable for standalone operation
    await runBot(app)

if __name__ == "__main__":
    try:
        # The runBot function uses async, so we use asyncio.run
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Telegram Bot stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
