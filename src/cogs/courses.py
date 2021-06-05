import discord
from discord.ext import commands
import os
import database.admindb


class Courses(commands.Cog):
    courses: list = []

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx: commands.Context, *, arg):
        if ctx.channel.name.endswith('bot-requests'):
            course = arg.upper()
            if database.admindb.course_exists(course, ctx.guild.id):
                category_name = course.split('-')[0]
                # Get or create original category
                category = discord.utils.get(
                    ctx.guild.categories, name=category_name)

                if category is None:
                    category = await ctx.guild.create_category(name=category_name)

                # Get or create second category if there are already over 50 channels in the original
                category = discord.utils.get(
                    ctx.guild.categories, name=category_name)
                if category is None:
                    category = await ctx.guild.create_category(name=category_name)

                channel = discord.utils.get(
                    ctx.guild.channels, name=course.lower())

                if channel is None:
                    channel = await ctx.guild.create_text_channel(course, category=category)
                    await channel.set_permissions(ctx.guild.default_role, read_messages=False)
                    await channel.set_permissions(self.client.user, read_messages=True)

                if channel.overwrites_for(ctx.message.author).read_messages == None:
                    await channel.set_permissions(ctx.message.author, read_messages=True)

                await ctx.message.channel.send('✅ Got it! Gave ' + ctx.message.author.mention + ' access to #' + course.lower() + '.')

                await channel.send(ctx.message.author.mention + ' joined the chat.')

            else:
                await ctx.message.channel.send('Course does not exist 🤦‍♀️')
        else:
            await ctx.message.channel.send('Use commands in bot-requests shithead 💩')

    @commands.command()
    async def leave(self, ctx: commands.Context, *, arg):
        if ctx.message.channel.name.endswith('bot-requests'):
            course = arg.upper()
            if database.admindb.course_exists(course, ctx.guild.id):
                channel = discord.utils.get(
                    ctx.guild.channels, name=course.lower())
                if channel.overwrites_for(ctx.message.author).read_messages != None:
                    await channel.set_permissions(
                        ctx.message.author, read_messages=None)
                    await ctx.message.channel.send("✅ Got it! Removed " + ctx.message.author.mention + "'s access to #" + course.lower() + ".")
                else:
                    await ctx.message.channel.send(ctx.message.author.mention + ", you are not in #" + course.lower() + " " + "😩")

            else:
                await ctx.message.channel.send('Course does not exist 🤦‍♀️')
        else:
            await ctx.message.channel.send('Use commands in bot-requests shithead 💩')

    @commands.command()
    async def ls(self, ctx):
        courses = database.admindb.course_list(ctx.guild.id)
        categories: typing.List[str] = []
        message: typing.List[str] = []
        [categories.append(course["category"])
            for course in courses if course["category"] not in categories]
        for category in categories:
            category_courses: typing.List[str] = []
            [category_courses.append(course["course_name"])
                for course in courses if course["category"] == category]
            category_msg: str = ""
            category_msg = category_msg + "**" + category + "**: "
            for course in category_courses:
                category_msg = category_msg + course.split('-')[1] + ", "
            category_msg = category_msg[:len(category_msg) - 2] + "\n"
            message.append(category_msg)
        optimized_message: typing.List[str] = []
        i: int = 0
        optimized_message.append("__Course List__\n")
        for x in message:
            if len(optimized_message[i]) + len(x) >= 2000:
                i = i + 1
                optimized_message.append(x)
            else:
                optimized_message[i] = optimized_message[i] + x
        for x in optimized_message:
            await ctx.message.channel.send(x)


def setup(client):
    client.add_cog(Courses(client))
