import discord
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions

import json
import os
from discord.ext import commands

client = discord.Client()


async def get_prefix(bot, message):
    return commands.when_mentioned_or(str('$'))(bot, message)

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

# Loop to look through cogs folder and load all cogs contained within it
for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'cogs')):
    if filename.endswith('.py'):
        # splicing cuts 3 last characters aka .py
        bot.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await bot.process_commands(message)

    if message.content.startswith('$ls'):
        await classPrint(message)

    if message.content.startswith('$help'):
        await helpPrint(message)


# Command helpers
async def classPrint(message):
    await message.channel.send(
        '>>> **The possible course channels to join are:**' +
        '\n\n**AERO**: 201, 290, 371, 390, 417, 431, 444, 446, 455, 462, 464, 465, 471, 472, 480, 481, 482, 483, 485, 486, 487, 490, GENERAL' +
        '\n**BCEE**: 231, 342, 343, 344, 345, 371, 451, 452, 455, 464, 465, 466' +
        '\n**BIOL**: 206, 261' +
        '\n**BLDG**: 212, 341, 365, 366, 371, 390, 462, 463, 465, 471, 472, 473, 474, 475, 476, 477, 478, 482, 490, 490A, 490B, 491, 492, 493, 498, GENERAL' +
        '\n**CHEM**: 205' +
        '\n**CIVI**: 212, 231, 321, 341, 361, 372, 381, 382, 390, 432, 435, 437, 440, 453, 454, 464, 465, 466, 467, 468, 469, 471, 474, 483, 484, 490, 498, GENERAL' +
        '\n**COEN**: 212, 231, 243, 244, 311, 313, 315, 316, 317, 320, 345, 346, 352, 390, 413, 421, 422, 424, 432, 433, 434, 445, 446, 447, 451, 490, 498, GENERAL' +
        '\n**COMP**: 108, 201, 208, 218, 228, 232, 233, 248, 249, 326, 333, 335, 339, 345, 346, 348, 352, 353, 354, 361, 367, 371, 376, 425, 426, 428, 432, 442, 444, ' +
        '445, 451, 465, 472, 473, 474, 476, 477, 478, 479, 490, 492, 495, 498, 499, 6231, 6721, GENERAL' +
        '\n**ECON**: 201, 203'
        '\n**ELEC**: 242, 251, 273, 275, 311, 312, 321, 331, 342, 351, 353, 365, 367, 372, 390, 413, 421, 422, 423, 424, 425, 430, 431, 432, 433, 434, 435, 435, 436, 437, ' +
        '438, 439, 440, 441, 442, 444, 445, 453, 455, 456, 457, 458, 463, 463, 463, 464, 465, 466, 470, 472, 473, 481, 482, 483, 490, 498, GENERAL' +
        '\n**ENCS**: 272, 282, 393, 483, 484, 498' +
        '\n**ENGR**: 108, 201, 202, 208, 213, 233, 242, 243, 244, 245, 251, 290, 301, 308, 311, 361, 371, 391, 392, 411, 412, 472, 490, 498' +
        '\n**IADI**: 301, 401')

    await message.channel.send(
        '>>> **INDU**: 211, 311, 320, 321, 323, 324, 330, 342, 371, 372, 410, 411, 412, 421, 423, 440, 441, 466, 475, 480, 490, 498, GENERAL' +
        '\n**MAST**: 218' +
        '\n**MECH**: 321, 343, 344, 351, 352, 361, 368, 370, 371, 375, 390, 411, 412, 414, 415, 421, 422, 423, 424, 425, 426, 444, 447, 448, 452, 453, 454, 460, 461, 462, 463, 471, ' +
        '\n472, 473, 474, 476, 490, 498, GENERAL' +
        '\n**MIAE**: 211, 215, 221, 311, 313, 380' +
        '\n**PHYS**: 205, 252, 284' +
        '\n**SOEN**: 228, 287, 321, 331, 341, 342, 343, 344, 345, 357, 363, 384, 385, 387, 390, 422, 423, 448, 449, 471, 487, 490, 491, 498, 499, 6441, GENERAL')


async def helpPrint(message):
    await message.channel.send(">>> **Hello:uwu:,I'm Coco:coconut:,your friendly neighbourhood bot:blueheart:**" +
                               "\n\nYou can use me to join class-specific channels." +
                               "\n\n**To JOIN a class:**" +
                               "\n:Check: `$join <code-####>`" +
                               "\n\n**To LEAVE a class:**" +
                               "\n:Cross: `$leave <code-####>`" +
                               "\n\n**Examples:**" +
                               "\n:small_blue_diamond: `$join comp-442`" +
                               "\n:small_blue_diamond: `$leave soen-228`" +
                               "\n\n**Notes:**" +
                               "\n:small_blue_diamond: Only __course-specific__ channels can be managed by me" +
                               "\n:small_blue_diamond: Use the $ls command to get a list of all permitted channels")

# Misc


async def isRoleInChannel(channel, course):
    for remainingMember in channel.members:
        memberRole = discord.utils.get(remainingMember.roles, name=course)
        if memberRole is not None:
            return True

    return False


async def getNumberOfCategoryChannels(category):
    count = 0
    for remainingChannel in category.channels:
        count = count + 1

    return count

client.run(os.getenv('BOT_TOKEN'))
