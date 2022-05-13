import os
from discord.ext import commands
from replit import db
from keep_alive import keep_alive
from cogs.prefix import get_prefix
import variables

admin = variables.admin

token = os.environ['TOKEN']
started_tasks = {}
print(db.keys())

client = commands.Bot(command_prefix=get_prefix)


@client.event
async def on_ready():
    print('Bot online: We have logged in as {0.user}'.format(client))
  
@client.command()
async def up(ctx):
    await ctx.reply("I'm up!", mention_author=False)

@client.command()
async def load(ctx, extension):
    if ctx.author.id in admin:
        client.load_extension(f"cogs.{extension}")
        await ctx.reply(f"Loading extension {extension}...", mention_author=False)

@client.command()
async def unload(ctx, extension):
    if ctx.author.id in admin:
        client.unload_extension(f"cogs.{extension}")
        await ctx.reply(f"Unloading extension {extension}...", mention_author=False)

@client.command()
async def reload(ctx, extension):
    if ctx.author.id in admin:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        await ctx.reply(f"Reloading extension {extension}...", mention_author=False)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

keep_alive()
client.run(token)
