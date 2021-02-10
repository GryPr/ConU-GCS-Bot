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

    sender = message.author

    args = message.content.split()

    # Join channel
    if message.content.startswith('$join '):
        if message.channel.name.endswith('bot-requests'):
            course = args[1].upper()
            if course in courses:
                role = discord.utils.get(guild.roles, name=course)
                channel = discord.utils.get(guild.channels, name=course.lower())
                bot_role = discord.utils.get(guild.roles, name='Coco')

                if role is None:
                    role = await guild.create_role(name=course)
                    channel = await guild.create_text_channel(course, category=category)
                    await channel.set_permissions(guild.default_role, read_messages=False)
                    await channel.set_permissions(bot_role, read_messages=True)
                    await channel.set_permissions(role, read_messages=True)

                category_name = course.split('-')[0]
                # Get or create original category
                category = discord.utils.get(guild.categories, name=category_name)

                if category is None:
                    category = await guild.create_category(name=category_name)

                # Get or create second category if there are already over 50 channels in the original
                if await getNumberOfCategoryChannels(category) == 50:
                    category = discord.utils.get(guild.categories, name=category_name + ' ')
                    if category is None:
                        category = await guild.create_category(name=category_name + ' ')

                if channel.category is not None:
                    if channel.category.name == 'recycling-bin':
                        await channel.edit(category=category)

                await sender.add_roles(role)

                await message.channel.send('Successively added user to course channel!')

            else:
                await message.channel.send('Error: course does not exist!')

    # Leave channel
    if message.content.startswith('$leave '):
        if message.channel.name == 'bot-requests':

            course = args[1].upper()
            if course in courses:
                role = discord.utils.get(guild.roles, name=course)
                channel = discord.utils.get(guild.channels, name=course.lower())

                recyclingBinCategory = discord.utils.get(guild.categories, name='recycling-bin')
                if recyclingBinCategory is None:
                    recyclingBinCategory = await guild.create_category(name='recycling-bin')

                if role is not None:
                    await sender.remove_roles(role)

                if channel is not None:
                    if not await isRoleInChannel(channel, course):
                        await channel.edit(category=recyclingBinCategory)


                await message.channel.send('Successively removed user from course channel!')

            else:
                await message.channel.send('Error: course does not exist!')


# Misc
@client.event
async def isRoleInChannel(channel, course):
    for remainingMember in channel.members:
        memberRole = discord.utils.get(remainingMember.roles, name=course)
        if memberRole is not None:
            return True

    return False

@client.event
async def getNumberOfCategoryChannels(category):
    count = 0
    for remainingChannel in category.channels:
        count = count + 1

    return count


with open('auth.json') as f:
    auth = json.load(f)
    client.run(auth['TOKEN'])
