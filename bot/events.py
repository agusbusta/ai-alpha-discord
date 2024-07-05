import os
import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot is ready as {self.bot.user}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        role = discord.utils.get(guild.roles, name="new-member")
        if role:
            await member.add_roles(role)
            verification_channel = discord.utils.get(guild.channels, id=int(os.getenv('VERIFICATION_CHANNEL_ID')))
            if verification_channel:
                verification_channel_mention = verification_channel.mention
                await member.send(f"Welcome to {guild.name}, {member.name}! Please complete the {verification_channel_mention} process to gain full access.")
            else:
                await member.send(f"Welcome to {guild.name}, {member.name}! Please complete the verification process to gain full access.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        channel = self.bot.get_channel(payload.channel_id)
        if channel and str(payload.emoji) == '✅':
            message = await channel.fetch_message(payload.message_id)
            if message.author == self.bot.user and message.content == "Please react to this message with a ✅":
                guild = self.bot.get_guild(payload.guild_id)
                if guild:
                    member = guild.get_member(payload.user_id)
                    if member:
                        verified_role = discord.utils.get(guild.roles, name="v-member")
                        if verified_role:
                            await member.add_roles(verified_role)
                            await member.send(f"You have been verified and given access to the server in {guild.name}!")
                            print(f"{member} changed their role to v-member after verification.")


async def setup(bot):
    await bot.add_cog(Events(bot)) 

