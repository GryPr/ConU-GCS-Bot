import discord
from discord.ext import commands
import os
import database.models
import database.admindb
import typing


class Admin(commands.Cog):
    templates: typing.List[str] = []

    def __init__(self, client):
        self.client = client
        self.db = database.models.db
        for filename in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'templates')):
            if filename.endswith('.txt'):
                self.templates.append(filename[:-4])

    @commands.command()
    async def addcourse(self, ctx, *args):
        argList: list = list(args)
        response: str = ""
        try:
            db_return: str = database.admindb.add_course(
                argList, ctx.guild.id)
            response = response + db_return + "\n"
        except BaseException as e:
            print(e)
        await ctx.message.channel.send(response)

    @commands.command()
    async def removecourse(self, ctx, *args):
        argList: list = list(args)
        response: str = ""
        try:
            db_return: str = database.admindb.remove_course(
                argList, ctx.guild.id)
            response = response + db_return + "\n"
        except BaseException as e:
            print(e)
        await ctx.message.channel.send(response)

    @commands.command()
    async def templatelist(self, ctx):
        response: str = "**Template List**\n"
        for template in self.templates:
            response = response + template + "\n"
        await ctx.message.channel.send(response)

    @commands.command()
    async def addtemplate(self, ctx, arg):
        response: str = ""
        if arg in self.templates:
            courses: typing.List[str] = []
            try:
                with open(os.path.join(os.path.dirname(__file__), '..', 'templates', arg + '.txt')) as fp:
                    line = fp.readline()
                    while line:
                        courses.append(line.strip())
                        line = fp.readline()
                    database.admindb.add_course(courses, ctx.guild.id)
            except BaseException as e:
                print(e)
            response = response + "✅ Added template " + arg
        else:
            response = response + "❌ Template does not exist"
        await ctx.message.channel.send(response)

    @commands.command()
    async def removetemplate(self, ctx, arg):
        response: str = ""
        if arg in self.templates:
            courses: typing.List[str] = []
            try:
                with open(os.path.join(os.path.dirname(__file__), '..', 'templates', arg + '.txt')) as fp:
                    line = fp.readline()
                    while line:
                        courses.append(line.strip())
                        line = fp.readline()
                    database.admindb.remove_course(courses, ctx.guild.id)
            except BaseException as e:
                print(e)
            response = response + "✅ Removed template " + arg
        else:
            response = response + "❌ Template does not exist"
        await ctx.message.channel.send(response)

    @commands.command()
    async def setprefix(self, ctx, arg):
        database.admindb.set_prefix(ctx.guild.id, arg)
        await ctx.message.channel.send("Changed prefix to " + arg)


def setup(client):
    client.add_cog(Admin(client))
