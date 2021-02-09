import discord
from discord.utils import get

import json

client = discord.Client()

courses = []
with open('courses.txt') as fp:
   line = fp.readline()
   while line:
       courses.append(line.strip())
       line = fp.readline()

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
            bot_role = discord.utils.get(guild.roles, name='Overwatch Hentai Bot')
            if role is None:
                role = await guild.create_role(name=course)
                print(guild.self_role)
                channel = await guild.create_text_channel(course, category=category)
                await channel.set_permissions(guild.default_role, read_messages=False)
                await channel.set_permissions(bot_role, read_messages=True)
                await channel.set_permissions(role, read_messages=True)

with open('auth.json') as f:
    auth = json.load(f)
    client.run(auth['TOKEN'])
