import requests
import time

import discord


class RedditPost:
    def __init__(self, channel, subreddit: str, sorting="hot", limit=15, debug=False):
        self.channel = channel
        self.subreddit = subreddit
        self.sorting = sorting
        self.limit = limit
        self.debug = debug

        try:
            with open(f"{self.subreddit}_last_post.txt", 'r') as save_file:
                self.last_post = save_file.readlines()
        except FileNotFoundError:
            self.last_post = []

    def __repr__(self) -> str:
        return f"RedditPost(# {self.channel.name}, r/{self.subreddit}, {self.sorting})"

    def load_listing(self) -> list:
        try:
            with open(f"{self.subreddit}_last_post.txt", 'r') as save_file:
                return save_file.read().splitlines()
        except FileNotFoundError:
            return []

    
    def get_listing(self) -> list:
        r = requests.get(f"https://www.reddit.com/r/{self.subreddit}/{self.sorting}/.json?limit={self.limit}",
                         headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})

        return r.json()["data"]["children"]    # returns a list

    def make_embed(self, post_json: dict) -> discord.Embed:
        """Takes a reddit post JSON and returns an discord Embed object from it's data"""
        post_data = post_json["data"]
        d_embed =  discord.Embed(type="rich",
                                title=post_data["title"],
                                description=post_data["selftext"],
                                url="https://www.reddit.com" + post_data["permalink"],
                                color=discord.Colour.from_rgb(201, 60, 252)
                                )

        d_embed.set_author(name=post_data["subreddit_name_prefixed"],
                           icon_url="https://cdn.discordapp.com/attachments/660584553513222147/808007886021066822/Es-jB0MU4AMmioi_3.jpeg",
                           url="https://www.reddit.com/r/" + post_data["subreddit"])
        
        d_embed.set_footer(text=':'.join([f"{i:02d}" for i in time.gmtime(post_data["created_utc"])[3:5]]))    # converts time format from Epoch to hour:minutes
        if not post_data["is_video"]:
            d_embed.set_image(url=post_data["url"]) if "comments" not in post_data["url"] else d_embed.set_image(url='')

        return d_embed

    async def send_embeds(self) -> None:
        """Retrieves new posts and send them in a discord channel and saves the name of the last post"""
        listing = self.get_listing()
        for post in listing[:-0:-1]:
            if post["data"]["stickied"] == False:    # "stickied" = pinned by moderator
                await self.channel.send(embed=self.make_embed(post))

        if len(listing[:-0:-1]) > 0:
            self.last_post = post["data"]["name"]
            with open(f"{self.subreddit}_last_post.txt", 'w') as save_file:
                save_file.write(self.last_post)
    
    async def send_save_embeds(self) -> None:
        listing = self.get_listing()
        previous_listing = self.load_listing()

        if self.debug:
            listing_names = [post["data"]["name"] for post in listing]
            print("\n************************************************************")
            print(':'.join([f"{i:02d}" for i in time.gmtime(time.time())[1:5]]))    # Time with month:day:hour:mins
            print(self)
            print(f"\n Length: {len(listing)}\n Results: {listing_names}\n")

        with open(f"{self.subreddit}_last_post.txt", 'w') as save_file:
            for post in listing[::-1]:
                if post["data"]["stickied"] == False:
                    save_file.write(post["data"]["name"] + '\n')
                    if post["data"]["name"] not in previous_listing:
                        try:
                            await self.channel.send(embed=self.make_embed(post))
                            if self.debug:
                                print("New post:", post["data"]["name"])
                        except:
                            pass

        if self.debug:
            print("\n************************************************************\n")
