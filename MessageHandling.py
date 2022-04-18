import discord
 
import asyncio
import datetime

import ctx_commands

from RedditPosting import RedditPost
from CommandHandler import ContextHandler, Context

DEBUG = False


class BaguetteClient(discord.Client):
    # self.postings = []

    def __init__(self, *, loop=None, **options):
        self.postings = []
        super().__init__(loop=loop, options=options)


    async def on_ready(self):
        self.main_handler = ContextHandler('!')
        print("Baguette Bot is connected", datetime.datetime.now())

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

        # uci_ch = self.get_channel(guild_id=660584553513222144, channel_id=730819065245073480)     # unused
        # art_ch = self.get_channel(guild_id=660584553513222144, channel_id=730070494291820555)     # unused
        space_ch = self.get_channel(guild_id=660584553513222144, channel_id=874633283122651147)
        animemes_ch = self.get_channel(guild_id=660584553513222144, channel_id=730980241065115689)
        cars_ch = self.get_channel(guild_id=660584553513222144, channel_id=965501399553151066)
        
        # postings.append(RedditPost(uci_ch, "UCI", "new"))
        self.postings.append(RedditPost(space_ch, "Astronomy"))
        self.postings.append(RedditPost(animemes_ch, "goodanimemes"))
        self.postings.append(RedditPost(cars_ch, "Miata"))

        while not self.is_closed():
            if DEBUG:
                print("Retrieving posts at ", datetime.datetime.now())

            for post in self.postings:
                await post.send_save_embeds()
            await asyncio.sleep(4200)

if __name__ == "__main__":
    with open("token.txt", 'r') as f:
        token = f.readline()
    client = BaguetteClient(max_messages=None)
    client.loop.create_task(client.reddit_posting())
    client.run(token)
