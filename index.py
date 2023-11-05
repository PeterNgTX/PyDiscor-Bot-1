import discord
import discord.ext

TOKEN = '<Bot Token>'

from typing import Literal, Optional
import discord
from discord.ext.commands import Greedy, Context
from discord import app_commands
from discord.ext import commands

#------ Bot ------
# Can add command_prefix='!discord commands.Bot() for Prefix Commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#--- Bot Startup
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}') #Bot Name
    print(bot.user.id) #Bot ID

#------ Slash Commands ------
#Parameters can be added in def help()
# Ex- async def help(interaction: discord.Interaction, left:int,right:int)

@bot.tree.command()
async def help(interaction: discord.Interaction):
    """Help""" #Description when viewing / commands
    await interaction.response.send_message("""

```It is Discord **Python** Language make by ||Beterng||

You can see it by click here```

""")

@bot.tree.command()
async def info(interaction: discord.Interaction):
    """About Bot""" #Description when viewing / commands
    await interaction.response.send_message("""
'''It is Discord **Python** Language make by ||Beterng||

You can see it by click here'''

""")

#------ Sync Tree ------
guild = discord.Object(id='1169765046713339935')
# Get Guild ID from right clicking on server icon
# Must have devloper mode on discord on setting>Advance>Developer Mode
#More info on tree can be found on discord.py Git Repo
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
    
bot.run(TOKEN)
