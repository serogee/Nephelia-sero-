from discord.ext import commands
import discord
from replit import db
import variables
import asyncio


default_prefix = variables.default_prefix
admin = variables.admin
bot_name = variables.bot_name
color = variables.color
bot_emoji = variables.bot_emoji



def get_prefix(client, message):
    if f"Prefix{str(message.guild.id)}" in db.keys():
        prefix = db[f"Prefix{str(message.guild.id)}"]
			
    else:
        db[f"Prefix{str(message.guild.id)}"] = default_prefix
        prefix = default_prefix
			
    return prefix
	
      

async def defprefix(self, message, admin, new_prefix=None):
    if new_prefix is None:
        mreply = message.reply
        mypfp = self.client.user.avatar_url
        prefix = db[f"Prefix{str(message.guild.id)}"]
        embed = discord.Embed(
        title="═════════\n**Help: __prefix__**\n═════════",
        description="```\n- Changes my prefix for this server\n```",
        color=color
        )
        embed.set_author(name=bot_name, icon_url=mypfp)
        embed.set_thumbnail(url=mypfp)
        embed.set_footer(text=f"{bot_emoji} {prefix}prefix {bot_emoji}")
        await mreply(embed=embed, mention_author=False)
    else:
        maid = message.author.id
        mreply = message.reply
        if maid in admin:
            db[f"Prefix{message.guild.id}"] = new_prefix
            await mreply(f'Successfully set my prefix for this server to **`{new_prefix}`**', mention_author=False)
        elif maid not in admin:
            await mreply('You do not have permission to change my prefix', mention_author=False)

class Prefix(commands.Cog):
  
    def __init__(self, client):
        self.client = client


      
    #events
    @commands.Cog.listener()
    async def on_message(self, message):
        mauthor = message.author
        cuser = self.client.user
        mcontent = message.content
        mcsplit = mcontent.split
        mgid = str(message.guild.id)
        mreply = message.reply
      
        if mauthor == cuser:
            return
      
        if cuser.mentioned_in(message):
            if "prefix" in mcontent:
                if f"Prefix{mgid}" in db.keys():
                    last_prefix = db[f"Prefix{mgid}"]
									
                else:
                    db[f"Prefix{mgid}"] = default_prefix
                    last_prefix = default_prefix
									
                prefix = mcsplit("prefix")[1]
							
                if str(prefix) == '':
                    await mreply(f"My current prefix for this server is **`{last_prefix}`**", mention_author=False)
                elif str(prefix).startswith(' '):
                    new_prefix = message.content.split("prefix ")[1]
                    await defprefix(self, message, admin, new_prefix)


    @commands.Cog.listener()
    async def on_guild_join(guild):
        db[f"Prefix{str(guild.id)}"] = default_prefix

    @commands.command()
    async def prefix(self, ctx, new_prefix=None):
        await defprefix(self, ctx, admin, new_prefix)
                  
def setup(client):
    client.add_cog(Prefix(client))