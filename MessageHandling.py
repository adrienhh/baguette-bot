import discord
 
import asyncio
import datetime

import ctx_commands

from bot_token import TOKEN
from RedditPosting import RedditPost
from CommandHandler import ContextHandler, Context


class BaguetteClient(discord.Client):
    async def on_ready(self):
        await client.change_presence(activity=discord.Game("with you"))
        self.main_handler = ContextHandler('!')
        print("Baguette Bot is connected", datetime.datetime.now())

        self.annonces_curb = self.get_channel(332667720523055114, 529655641288212492)

    def get_guild(self, guild_id):
        for guild in self.guilds:
            if guild.id == guild_id:
                return guild

    def get_channel(self, guild_id, channel_id):
        for channel in self.get_guild(guild_id).channels:
            if channel.id == channel_id:
                return channel

    async def on_message(self, message):
        if message.author == self.user:
            return

        ctx = Context(message)
        self.main_handler.set_context(ctx)

        await self.main_handler.execute(ctx_commands)

    async def reddit_posting(self):
        await self.wait_until_ready()

        uci_channel = self.get_channel(guild_id=660584553513222144,
                                       channel_id=730819065245073480)           # UCI BTS
        uci = RedditPost(uci_channel, "UCI", "new")

        animemes_channel = self.get_channel(guild_id=660584553513222144,
                                            channel_id=730980241065115689)      # Animemes
        animemes = RedditPost(animemes_channel, "Animemes")
        goodanimemes = RedditPost(animemes_channel, "goodanimemes")

        while not self.is_closed():
            print("Retrieving posts at ", datetime.datetime.now())
            await uci.send_save_embeds()
            await animemes.send_save_embeds()
            await goodanimemes.send_save_embeds()

            await asyncio.sleep(4200)

if __name__ == "__main__":
    client = BaguetteClient(max_messages=None)
    client.loop.create_task(client.reddit_posting())
    client.run(TOKEN)
    print("It has somehow ended", datetime.datetime.now())
