import discord
from discord.utils import get

import json

client = discord.Client()

courses = ['comp-420', 'comp-69']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    guild = message.guild

    if message.author == client.user:
        return

    category = discord.utils.get(guild.categories, name='courses')

    if category is None:
        category = await guild.create_category(name='courses')

    if message.content.startswith('!roles'):
        for course in courses:
            role = discord.utils.get(guild.roles, name=course)
            if role is None:
                role = await guild.create_role(name=course)
                permissions = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True),
                    role: discord.PermissionOverwrite(read_messages=True)
                }
                channel = await guild.create_text_channel(course, override=permissions, category=category)

with open('auth.json') as f:
    auth = json.load(f)
    client.run(auth['TOKEN'])
