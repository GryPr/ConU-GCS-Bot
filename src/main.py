import discord
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions

import json
import os
from discord.ext import commands


async def get_prefix(bot, message):
    return commands.when_mentioned_or('$')(bot, message)

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Command is missing arguments 😪')
    else:
        await ctx.send('An unknown error has occured 👀')

# Loop to look through cogs folder and load all cogs contained within it
for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'cogs')):
    if filename.endswith('.py'):
        # splicing cuts 3 last characters aka .py
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run(os.getenv('BOT_TOKEN'))
