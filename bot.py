import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Configura el bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Carga los módulos (cogs)
initial_extensions = ['routes.welcome']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Ejecuta el bot
bot.run(os.getenv('DISCORD_TOKEN'))
