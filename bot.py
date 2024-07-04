import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from config.settings import WELCOME_CHANNEL_ID, VERIFICATION_CHANNEL_ID, PUBLIC_CHANNEL_ID, DISCORD_TOKEN

load_dotenv()


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MEMBER_ROLE_NAME = 'member'
NEW_MEMBER_ROLE_NAME = 'new-member'
WELCOME_CHANNEL_ID2 = int(os.getenv('WELCOME_CHANNEL_ID'))


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot Connected as {bot.user}')
    for guild in bot.guilds:
        await create_default_roles_if_not_exist(guild)
        await pin_welcome_message(guild)

async def create_default_roles_if_not_exist(guild):
    roles_to_create = [NEW_MEMBER_ROLE_NAME, MEMBER_ROLE_NAME]
    for role_name in roles_to_create:
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if not existing_role:
            try:
                await guild.create_role(name=role_name)
                print(f"Created '{role_name}' role in {guild.name}")
            except discord.Forbidden:
                print(f"No permission to create '{role_name}' role in {guild.name}")
            except discord.HTTPException:
                print(f"Failed to create '{role_name}' role in {guild.name}")

async def pin_welcome_message(guild):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        messages = [message async for message in channel.history(limit=10)]
        for message in messages:
            if message.author == bot.user and "START HERE" in message.content:
                await message.pin()
                return
        welcome_message = await channel.send("Welcome to the server! Please START HERE.")
        await welcome_message.pin()

@bot.event
async def on_member_join(member):
    new_member_role = discord.utils.get(member.guild.roles, name=NEW_MEMBER_ROLE_NAME)
    if new_member_role:
        await member.add_roles(new_member_role)
    
    try:
        await member.send(f'Hi {member.name}, welcome to our Discord server! Please verify yourself in the {bot.get_channel(VERIFICATION_CHANNEL_ID).mention} channel.')
    except discord.errors.Forbidden:
        print(f"Couldn't send DM to {member.name}")

    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if welcome_channel:
        embed = discord.Embed(
            description=f'Welcome **{member.mention}** to the server!',
            color=0xFFFFFF,  
            timestamp=datetime.datetime.now()
        )
        await welcome_channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def verify(ctx, member: discord.Member):
    new_member_role = discord.utils.get(ctx.guild.roles, name=NEW_MEMBER_ROLE_NAME)
    member_role = discord.utils.get(ctx.guild.roles, name=MEMBER_ROLE_NAME)
    
    if new_member_role in member.roles:
        await member.remove_roles(new_member_role)
        await member.add_roles(member_role)
        await ctx.send(f"{member.mention} has been verified and given the '{MEMBER_ROLE_NAME}' role.")
    else:
        await ctx.send(f"{member.mention} does not have the '{NEW_MEMBER_ROLE_NAME}' role.")

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)