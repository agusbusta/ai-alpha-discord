import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

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
    
    # Buscar el mensaje existente de verificación
    async for message in verification_channel.history(limit=50):  # Busca los últimos 50 mensajes
        if message.author == bot.user and message.content == "Please react to this message with a ✅":
            print("Verification message found.")
            return message
    
    # Si no se encuentra el mensaje, crear uno nuevo
    print("Creating new verification message.")
    return await verification_channel.send("Please react to this message with a ✅")

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="!help for commands"))
    print("Bot is online and ready!")
    
    # Configurar el mensaje de verificación al iniciar el bot
    await setup_verification_message()

@bot.event
async def on_raw_reaction_add(payload):
    # Verificar si la reacción fue en el mensaje de verificación y con el emoji correcto
    if payload.emoji.name == '✅':
        VERIFICATION_CHANNEL_ID = int(os.getenv('VERIFICATION_CHANNEL_ID'))
        verification_channel = bot.get_channel(VERIFICATION_CHANNEL_ID)
        if not verification_channel:
            print(f"Verification channel with ID {VERIFICATION_CHANNEL_ID} not found.")
            return
        
        message = await verification_channel.fetch_message(payload.message_id)
        if message.author == bot.user and message.content == "Please react to this message with a ✅":
            guild = bot.get_guild(payload.guild_id)
            if guild:
                member = guild.get_member(payload.user_id)
                if member:
                    verified_role = discord.utils.get(guild.roles, name="v-member")
                    if verified_role:
                        await member.add_roles(verified_role)
                        print(f"{member} changed their role to v-member after verification.")

async def start_bot():
    await bot.start(os.getenv('DISCORD_TOKEN'))



if __name__ == "__main__":
    import asyncio
    from events import setup

    asyncio.run(setup(bot))
    asyncio.run(start_bot())  # Utilizar asyncio.run para ejecutar de manera asincrónica
 # Utilizar asyncio.run para ejecutar de manera asincrónica
