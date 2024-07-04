import datetime
import discord
from discord.ext import commands
from discord.utils import get
from config.settings import WELCOME_CHANNEL_ID, VERIFICATION_CHANNEL_ID, MEMBER_ROLE_NAME, NEW_MEMBER_ROLE_NAME

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot Connected as {self.bot.user}')
        for guild in self.bot.guilds:
            await self.create_default_roles_if_not_exist(guild)
            await self.pin_welcome_message(guild)

    async def create_default_roles_if_not_exist(self, guild):
        roles_to_create = [NEW_MEMBER_ROLE_NAME, MEMBER_ROLE_NAME]
        for role_name in roles_to_create:
            existing_role = get(guild.roles, name=role_name)
            if not existing_role:
                try:
                    await guild.create_role(name=role_name)
                    print(f"Created '{role_name}' role in {guild.name}")
                except discord.Forbidden:
                    print(f"No permission to create '{role_name}' role in {guild.name}")
                except discord.HTTPException:
                    print(f"Failed to create '{role_name}' role in {guild.name}")

    async def pin_welcome_message(self, guild):
        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            messages = [message async for message in channel.history(limit=10)]
            for message in messages:
                if message.author == self.bot.user and "START HERE" in message.content:
                    await message.pin()
                    return
            welcome_message = await channel.send("Welcome to the server! Please START HERE.")
            await welcome_message.pin()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        new_member_role = get(member.guild.roles, name=NEW_MEMBER_ROLE_NAME)
        if new_member_role:
            await member.add_roles(new_member_role)

        try:
            await member.send(f'Hi {member.name}, welcome to our Discord server! Please verify yourself in the {self.bot.get_channel(VERIFICATION_CHANNEL_ID).mention} channel.')
        except discord.errors.Forbidden:
            print(f"Couldn't send DM to {member.name}")

        welcome_channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if welcome_channel:
            embed = discord.Embed(
                description=f'Welcome **{member.mention}** to the server!',
                color=0xFFFFFF,
                timestamp=datetime.datetime.now()
            )
            await welcome_channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def verify(self, ctx, member: discord.Member):
        new_member_role = get(ctx.guild.roles, name=NEW_MEMBER_ROLE_NAME)
        member_role = get(ctx.guild.roles, name=MEMBER_ROLE_NAME)

        if new_member_role in member.roles:
            await member.remove_roles(new_member_role)
            await member.add_roles(member_role)
            await ctx.send(f"{member.mention} has been verified and given the '{MEMBER_ROLE_NAME}' role.")
        else:
            await ctx.send(f"{member.mention} does not have the '{NEW_MEMBER_ROLE_NAME}' role.")

def setup(bot):
    bot.add_cog(Welcome(bot))
