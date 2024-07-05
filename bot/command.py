import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

class VerifyButton(discord.ui.Button):
    def __init__(self):
        super().__init__(emoji="✅")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Check your DMs for verification steps.", ephemeral=True)
        await interaction.user.send("Please click the ✅ button below to verify.")

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx):
        VERIFICATION_CHANNEL_ID = int(os.getenv('VERIFICATION_CHANNEL_ID'))
        if ctx.channel.id != VERIFICATION_CHANNEL_ID:
            await ctx.send("This command can only be used in the verification channel.")
            return

        button = VerifyButton()
        view = discord.ui.View()
        view.add_item(button)
        await ctx.send("Click the button below to start the verification process:", view=view)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("Verification successful!"):
            user_id = int(message.content.split()[-1])
            user = await self.bot.fetch_user(user_id)
            guild = self.bot.get_guild(int(os.getenv('GUILD_ID')))
            new_user_role_name = "New User"
            verified_user_role_name = "Verified User"

            if guild:
                new_user_role = discord.utils.get(guild.roles, name=new_user_role_name)
                verified_user_role = discord.utils.get(guild.roles, name=verified_user_role_name)
                member = guild.get_member(user.id)

                if new_user_role and verified_user_role and member:
                    await member.remove_roles(new_user_role)
                    await member.add_roles(verified_user_role)
                    await member.send("You have been verified and given access to the server!")

                    verification_channel = self.bot.get_channel(1258501353572143255)
                    if verification_channel:
                        await verification_channel.send(f"{user.mention} has been verified!")

                    print(f"{user.name} changed their role from {new_user_role_name} to {verified_user_role_name}")

async def setup(bot):
    bot.add_cog(Commands(bot))
