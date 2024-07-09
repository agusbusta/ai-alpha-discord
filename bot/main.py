import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from utls import check_email_in_database

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def setup_verification_message():
    VERIFICATION_CHANNEL_ID = int(os.getenv('VERIFICATION_CHANNEL_ID'))
    verification_channel = bot.get_channel(VERIFICATION_CHANNEL_ID)
    if not verification_channel:
        print(f"Verification channel with ID {VERIFICATION_CHANNEL_ID} not found.")
        return
    
    async for message in verification_channel.history(limit=50):
        if message.author == bot.user and message.content == "Please react to this message with a ✅":
            print("Verification message found.")
            return message
    
    print("Creating new verification message.")
    return await verification_channel.send("Please react to this message with a ✅")

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="!help for commands"))
    print("Bot is online and ready!")
    await setup_verification_message()

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    channel = bot.get_channel(payload.channel_id)
    if channel and str(payload.emoji) == '✅':
        message = await channel.fetch_message(payload.message_id)
        if message.author == bot.user and message.content == "Please react to this message with a ✅":
            guild = bot.get_guild(payload.guild_id)
            if guild:
                member = guild.get_member(payload.user_id)
                if member:
                    verified_role = discord.utils.get(guild.roles, name="v-member")
                    if verified_role:
                        await member.add_roles(verified_role)
                        await member.send("You have been verified! Please reply with your email address to complete the next step.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.type == discord.ChannelType.private:
        email = message.content.strip()
        if check_email_in_database(email):
            print("User was found in db, now receives the Founder member role")
            role = discord.utils.get(message.guild.roles, name="founder-member")
        else:
            print("User was not found in db, now receives the new-to-founder-member Role")
            role = discord.utils.get(message.guild.roles, name="new-to-founder-member")
        
        if role:
            await message.author.add_roles(role)
            await message.channel.send(f"You have been assigned the role: {role.name}")


async def start_bot():
    await bot.start(os.getenv('TOKEN_DS'))

if __name__ == "__main__":
    import asyncio
    from events import setup

    asyncio.run(setup(bot))
    asyncio.run(start_bot()) 