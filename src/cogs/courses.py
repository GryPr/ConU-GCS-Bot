import discord
from discord.ext import commands
import os


class Courses(commands.Cog):
    courses = []

    def __init__(self, client):
        self.client = client
        with open(os.path.join(os.path.dirname(__file__), '..', 'resources/courses.txt')) as fp:
            line = fp.readline()
            while line:
                self.courses.append(line.strip())
                line = fp.readline()

    @commands.command()
    async def join(self, ctx, *, arg):
        if ctx.channel.name.endswith('bot-requests'):
            course = arg
            if course in self.courses:
                category_name = course.split('-')[0]
                # Get or create original category
                category = discord.utils.get(
                    ctx.guild.categories, name=category_name)

                if category is None:
                    category = await ctx.guild.create_category(name=category_name)

                # Get or create second category if there are already over 50 channels in the original
                category = discord.utils.get(
                    ctx.guild.categories, name=category_name + ' ')
                if category is None:
                    category = await ctx.guild.create_category(name=category_name + ' ')

                channel = discord.utils.get(
                    ctx.guild.channels, name=course.lower())

                if channel is None:
                    channel = await ctx.guild.create_text_channel(course, category=category)
                    await channel.set_permissions(ctx.guild.default_role, read_messages=False)
                    await channel.set_permissions(self.client.user, read_messages=True)

                if channel.overwrites_for(ctx.message.author).read_messages == None:
                    await channel.set_permissions(ctx.message.author, read_messages=True)

                await ctx.message.channel.send(':white_check_mark: Got it! Gave ' + ctx.message.author.mention + ' access to #' + course.lower() + '.')

                await ctx.channel.send(ctx.message.author.mention + ' joined the chat.')

            else:
                await ctx.message.channel.send('Error: course does not exist!')

    @commands.command()
    async def leave(self, ctx, *, arg):
        if ctx.message.channel.name.endswith('bot-requests'):
            course = arg
            if course in self.courses:
                channel = discord.utils.get(
                    ctx.guild.channels, name=course.lower())
                if channel.overwrites_for(ctx.message.author).read_messages != None:
                    await channel.set_permissions(
                        ctx.message.author, read_messages=None)
                    await ctx.message.channel.send(":white_check_mark: Got it! Removed " + ctx.message.author.mention + "'s access to #" + course.lower() + ".")
                else:
                    await ctx.message.channel.send(ctx.message.author.mention + ", you are not in #" + course.lower() + ".")

            else:
                await ctx.message.channel.send('Error: course does not exist!')


def setup(client):
    client.add_cog(Courses(client))
