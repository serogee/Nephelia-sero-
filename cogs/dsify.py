from discord.ext import commands
from replit import db
import discord 
import variables
import re
import asyncio
import random

admin = variables.admin
bot_name = variables.bot_name
color = variables.color
bot_emoji = variables.bot_emoji

context = ["dsify","d", "ds", "$ify", "$"]
aliases = ["d", "ds", "$ify", "$"]
sleep_time = [1, 1.5, 1.2, 0.8, 2.1, 2.5, 1.3]
ugly_reply = ["I don't really wanna show you such an abomination", "It's _definitely_ not the prettiest thing in the world", "Just forget about it", "It's a mess", "I doubt you'd want to use that mess"]
empty_text_reply = ["Wow, that's as empty as my soul... before I met Zagan-sama that is.", "Empty... Perfectly describes a certain someone's will to live", "Wow.", "Well that's pretty fuckin' empty aint it", "You know, there's a saying... If life doesn't kill you, emptiness will.", "How empty.", "Awesome.", "...Well that's pretty useless. What were you trying to do?", "I'm starting to think you're just doing this out of spite", "I don't really have much replies for this"]

def dsify_embed(mypfp, prefix):
        embed = discord.Embed(
            title="═════════\n**Help: __dsify__**\n═════════",
            description="- Converts copied list from mudae into a usable format with `$` at the end of each item\n\u200b",
            color=color
        )
        embed.set_author(name=bot_name, icon_url=mypfp)
        embed.set_thumbnail(url=mypfp)
        embed.add_field(name="__Primary Flags (Modes)__", value="\
                        **\u200b> r**\
                        \nAdds `$` in between items. Use with `v` flag in a Mudae list. (ie. `$mmv`, `$fnv`)\
                        \n \
                        \n**\u200b> a**\
                        \nFixes and adds `$` in between itemsfor Mudae lists with flags `a` and `b`. (ie. `$mmab`, `$fnab`)\n \n**\u200b> l**\
                        \nFixes and adds `$` in between items for `$llanim` and `$llgame`.\
                        \n \
                        \n**\u200b> p**\
                        \nFixes and adds `$` in between items in `$mpd` and `$mpdo` for pin trading. \
                        \n\u200b", inline=False)
        embed.add_field(name="__Optional Flags__", value="\
                        **\u200b> c** \
                        \nCompacts everything instead of creating new lines.\
                        \n \
                        \n**\u200b> e** \
                        \nCompact without spaces (overrides the c flag) \
                        \n \
                        \n**\u200b> d** \
                        \nDeletes command.\
                        \n \
                        \n**\u200b> x** \
                        \nAdds `--` to the start of every item\
                        \n\u200b", inline=False)
        embed.add_field(name="__Examples__", value=f"```\
                        \n{prefix}dsifyr [List from $llv]\
                        \n``` ```\
                        \n{prefix}dsifysd [List from $wlab]\
                        \n``` ```\
                        \n{prefix}dsifypc [List from $mpdo @other_user]\
                        \n```", inline=False)
        embed.set_footer(text= f"{bot_emoji} {prefix}dsify {bot_emoji}" )
        return embed

def paginate(temp_list, maxchars=1800):
    size = 0
    message_text = []
    for item in temp_list:
        if len(item) + size > maxchars:
            yield message_text
            message_text = []
            size = 0
        message_text.append(item)
        size += len(item)
    yield message_text
        
async def dsify_flagger(client, alias, msg):
    mgid = msg.guild.id
    str_mgid = str(mgid)
    prefix = f"Prefix{str_mgid}"
    prefix = db[prefix]
    rcommand_split = msg.content.replace(f"{prefix}{alias}", "")
    rcommand_split = rcommand_split.split(" ")
    flags = rcommand_split[0]
    mcontent_split = msg.content.split(f"{prefix}{alias}{flags}")
    text = mcontent_split[1]
    msend = msg.channel.send    
    mauthor = msg.author
    pfp = mauthor.avatar_url
    author = f"{str(mauthor.name)}#{str(mauthor.discriminator)}"

    f = re.compile(r"\$\D+")
    com = f.search(flags)
    if com:
        flags = f.sub("", flags)
        com = com.group(0)
        com = f"{com} "
    if not com:
        com = ""

    modes = []
    mode_flags = ["a", "r", "l", "p"]

    for mode_flag in mode_flags:
        mode_flags.append(mode_flag)

    if len(modes) != 1 and flags != "":
        if len(modes) == 0:  
            mypfp = str(client.user.avatar_url)
            embed = dsify_embed(mypfp, prefix)
            await msg.reply(embed=embed, mention_author=False)
            return
            
        if len(modes) > 1 and "prefix" not in msg.content:
            await msg.reply("Please pick only one mode! I tried to convert it, and... well...", mention_author=False)
            await asyncio.sleep(random.choice(sleep_time))
            await msend(random.choice(ugly_reply))
            return

    #joiner, flags
    joiner = "$\n"
    if "joiner=" in text:
        joiner = text.split("joiner=")[1]
        text.replace("joiner=", "")
    if "c" in flags:
        joiner = " $ "
    if "e" in flags:
        joiner = "$"
    anti = False
    if "x" in flags:
        anti = True
    deleteme = False
    if "d" in flags:
        await msg.delete()
        deleteme = True
    delete = False
    if "dd" in flags:
        delete = True
    if "w" in flags:
        if not deleteme:
            await msg.reply("Alright, I'll wait until you finish (send `&` to end)", mention_author=False)
        def check(message):
            return message.author == msg.author and message.channel == msg.channel
        while True:
            message = await client.wait_for("message", timeout=60, check=check)
            if message:
                if message.content.startswith(prefix):
                    if not deleteme:
                        await msend("On it.")
                    if deleteme:
                        await message.delete()
                    break 
                else:
                    if text != "":
                        text = f"{text}\n{message.content}"
                        if deleteme:
                            await message.delete()
                        elif not deleteme:
                            await message.reply("Added", mention_author=False)
                    elif text == "":
                        text = f"{message.content}"
                        if deleteme:
                            await message.delete()
                        elif not deleteme:
                            await message.reply("Added", mention_author=False)
            elif message is None:
                await msend("Nothing else? I don't like waiting this long. I'll just assume that that's all.")
                break

    #anti-noise
    text = text.replace('\u200b\n', '')
    text = text.replace(" no_entry_sign $wa DISABLED", "")
    text = text.replace(" no_entry_sign $wg DISABLED", "")
    text = text.replace(" no_entry_sign $hg DISABLED", "")
    text = text.replace(" no_entry_sign $ha DISABLED", "")
    text = text.replace(' - ', '\no98786Ghg09')
    text = text.replace('\n\n', '\n')
    text = text.replace('\u200b', '')
    if text.startswith(" "):
        text.replace(" ", "", 1)
    if text.startswith("\n"):
        text.replace("\n", "", 1)


    #prep 
    temp_list = []
    mode = None
    splitted_text = text.split("\n")

    
    #flag mode (regular, series, likelist)
    if "r" in flags:
        mode = "Regular"
        for item in splitted_text:
            if anti:
                item = "--" + item
            temp_list.append(item)
    if "a" in flags:
        modes.append("Series")
        mode = "Series"
        for item in splitted_text:
            if "o98786Ghg09" not in item:
                if item.startswith(" "):
                    item = item.replace(" ", "", 1)
                if anti:
                    item = "--" + item
                temp_list.append(item)
    if "l" in flags:
        mode = "Likelist"
        for item in splitted_text:
            match = (re.search(r'\d+', item))
            if match:
                item = item.replace(str(match.group(0)) + ". ", "")
                if item.startswith(" "):
                    item = item.replace(" ", "", 1)
                if anti:
                    item = "--" + item
                temp_list.append(item)
            elif not match:
                if anti:
                    item = "--" + item
                temp_list.append(item)
    if "p" in flags:
        mode = "Pins"
        text = text.replace("\n", "")
        text = text.replace(" ", "")
        text = re.sub(r"x\d+", "", text)
        item_split = re.findall(r"[^x0-9]+\d+", text)
        for item in item_split:
            if "pin" in item:
                temp_list.append(item)

    #joiner and sender 

    footer = f"{bot_emoji} {prefix}dsify {mode} {bot_emoji}" 
    embed = discord.Embed(color=color)
    embed.set_author(name=author, icon_url=pfp)
    embed.set_footer(text=footer)
    
    for message_text in paginate(temp_list):
        embed.description = com + joiner.join(message_text)
        if deleteme:
            mymsg = await msend(embed=embed)
            if delete:
                await mymsg.add_reaction("❌")
        elif not deleteme:
            await msg.reply(embed=embed, mention_author=False)


    #returning
    return 
    
        
    

class DSify(commands.Cog):

	  
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        client = self.client
        cuser = client.user
        mauthor = message.author
        mcontent = message.content
        mgid = message.guild.id
        str_mgid = str(mgid)
        prefix = f"Prefix{str_mgid}"
        prefix = db[prefix]
        
        if mauthor == cuser:
            return

        for alias in context:
            if f"{prefix}{alias}" in mcontent and mcontent.split(f"{prefix}{alias}")[1] != "":
                await dsify_flagger(client, alias, message)
                break

        
    @commands.command(pass_context=True, aliases=aliases)
    async def dsify(self, ctx):
        cuser = self.client.user
        mypfp = str(cuser.avatar_url)
        mgid = str(ctx.message.guild.id)
        prefix = db[f"Prefix{mgid}"]
        embed = dsify_embed(mypfp, prefix)
        await ctx.reply(embed=embed, mention_author=False)
                      

def setup(client):
    client.add_cog(DSify(client))