import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID", "27383453")
API_HASH = os.getenv("API_HASH", "4c246fb0c649477cc2e79b6a178ddfaa")
BOT_TOKEN = os.getenv("BOT_TOKEN", "6918499458:AAFtXeIJ9sdXAuHk7tGAcrU5OTF1KYMZebk")
SUDOERS = list(map(int, os.getenv("SUDOERS", "6762113050").split()))
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://SHASHANK:STRANGER@shashank.uj7lold.mongodb.net/?retryWrites=true&w=majority")
LOG_GROUP_ID = os.getenv("LOG_GROUP_ID", "-1002018556839")
MUST_JOIN = os.getenv("MUST_JOIN", "SHIVANSH474")
DISABLED = os.getenv("DISABLED", "").split()

if not API_ID:
    raise SystemExit("No API_ID found. Exiting...")
elif not API_HASH:
    raise SystemExit("No API_HASH found. Exiting...")
elif not BOT_TOKEN:
    raise SystemExit("No BOT_TOKEN found. Exiting...")

if not MONGO_URL:
    print("MONGO_URL environment variable Is Empty Bot")

# Convert the LOG_GROUP_ID variable to an integer if it is not None
if LOG_GROUP_ID:
    LOG_GROUP_ID = int(LOG_GROUP_ID)
