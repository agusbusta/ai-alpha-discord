from dotenv import load_dotenv
import os

load_dotenv()

# Discord bot token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID'))
VERIFICATION_CHANNEL_ID = int(os.getenv('VERIFICATION_CHANNEL_ID'))
PUBLIC_CHANNEL_ID = int(os.getenv('PUBLIC_CHANNEL_ID'))
MEMBER_ROLE_NAME = 'member'
NEW_MEMBER_ROLE_NAME = 'new-member'


