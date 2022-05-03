"""Module that groups all functions that are interpreted as commands by the CommandHandler"""

import discord
import random

BOT_OWNER_ID = 153134879717064704


async def ping(ctx):
    """Simple response command"""
    await ctx.send("Pong")


async def avatar(ctx, name=''):
    """Command that sends the url of the author's avatar (no arguments) or the user in the guild with 'name'"""
    if ctx.author.display_name == name or name == '' or ctx.author.mention == name:
        await ctx.channel.send(ctx.author.avatar_url)
    else:
        for member in ctx.guild.members:
            if member.display_name == name or member.name == name or member.mention == name:
                await ctx.channel.send(member.avatar_url)


def _has_mention(mention):
    def inner(message):
        return f"<@{message.author.id}>" == mention if mention != None else True
    return inner


async def purge(ctx, num:int, mention=None):
    # TODO: limit != number of messages that will get deleted. Make way to guarantee the number of messages deleted
    try:
        num = int(num)
        if "Baguette" in [role.name for role in ctx.author.roles]:
            await ctx.channel.purge(limit=num + 1, check=_has_mention(mention))
    except discord.Forbidden:
        await ctx.send("Bot does not have permission to manage messages.")


async def coinflip(ctx):
    await ctx.send("Heads") if random.choice([0, 1]) == 0 else await ctx.send("Tails")


async def choice(ctx, *args):
    """Chooses one word among a list of given arguments (whitespace separated)"""
    await ctx.send(random.choice(args))


async def supermute(ctx):
    """Mutes every user currently in a voice channel"""
    if "Baguette" in [role.name for role in ctx.author.roles]:
        for member in ctx.guild.members:
            try:
                if member.voice != None:
                    await member.edit(mute=True)
            except discord.Forbidden:
                pass


async def unmute(ctx):
    """Unmutes every user currently in a voice channel"""
    if "Baguette" in [role.name for role in ctx.author.roles]:
        for member in ctx.guild.members:
            try:
                if member.voice != None:
                    await member.edit(mute=False)
            except discord.Forbidden:
                pass


async def die(ctx):
    """Terminates the bot if command sent by bot owner"""
    if ctx.author.id == BOT_OWNER_ID:
        await ctx.send("Time to sleep")
        exit()
