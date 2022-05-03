import discord
 
import asyncio
import datetime
import argparse
import json

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

    async def guild_posting_subs(self, config_json):
        await self.wait_until_ready()

        if DEBUG:
            print("LOADING CONFIG")

        for guild in config_json["guilds"]:
            if DEBUG:
                print(f"In guild: {self.get_guild(guild['id']).name}")

            for posting in guild["postings"]:
                channel = self.get_channel(guild_id=guild["id"], channel_id=posting["channel_id"])
                if DEBUG:
                    print(f" In channel: {channel.name}")

                if posting["has_custom_sorting"]:
                    # A config file with "has_custom_sorting": true allows for more detailed listing options
                    for subreddit in posting["subreddits"]:
                        if DEBUG:
                            print(f"  Subscribed to subreddit: {subreddit['name']} with {subreddit['sorting']} sorting")
                        self.postings.append(RedditPost(channel, subreddit["name"], subreddit["sorting"]))
                else:
                    # but since "hot" is the most interesting listing we accept it as default
                    # it allows users to write simpler config files (and just list names of subreddits)
                    for subreddit in posting["subreddits"]:
                        if DEBUG:
                            print(f"  Subscribed to subreddit: {subreddit}")
                        self.postings.append(RedditPost(channel, subreddit))

        # Check listings for subscribed subreddits and send post in channels
        while not self.is_closed():
            if DEBUG:
                print(f"Retrieving posts at {datetime.datetime.now()}")

            for post in self.postings:
                await post.send_save_embeds()
            await asyncio.sleep(config_json["delay"])


if __name__ == "__main__":
    client = BaguetteClient(max_messages=None)

    # Initializing parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Read config for subreddits in a JSON file")
    parser.add_argument("-v", "--verbose", action="store_true", help="execute program in verbose mode (debugging)")

    # Parsing args
    parsed_args = parser.parse_args()
    
    DEBUG = parsed_args.verbose

    # Reading subreddit config file
    if parsed_args.config != None:
        with open(parsed_args.config, 'r') as f:
            config_json = json.load(f)
        client.loop.create_task(client.guild_posting_subs(config_json))

    # Token cannot be kept in code so we read it from a file
    with open("token.txt", 'r') as f:
        token = f.readline()

    client.run(token)
