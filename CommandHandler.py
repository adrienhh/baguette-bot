import discord
import inspect


class Context:
    def __init__(self, message):
        """
        An imitation of the Context class offered in discord.ext commands which
        regroup message, guild and channel with a little bit more useful variables
        in a single class
        """
        # The most useful data
        self.message = message
        self.guild = message.guild
        self.channel = message.channel
        self.author = message.author

        self.content = message.content

        self.cmd_main, self.cmd_args = self.get_cmd_and_args()

    def get_cmd_and_args(self) -> (str, [str]):
        content_list = self.message.content.split()
        if len(content_list) > 0:
            return (content_list[0], [v for i, v in enumerate(content_list) if i > 0])
        else:
            return '', ''

    async def send(self, message: str, *, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None):
        """This is ass"""
        await self.channel.send(message,
                                tts=tts, 
                                embed=embed, 
                                file=file, 
                                files=files, 
                                delete_after=delete_after, 
                                nonce=nonce)


class CommandHandler:
    def __init__(self, prefix='', message=None):
        """Old Implementation with Messages, use Context instead"""
        self.prefix = prefix
        self.message = message

        self.cmd_main = ''
        self.cmd_args = ''
        
        content_list = self.message.content.split()
        if len(content_list) > 0:
            self.cmd_main = content_list[0]
            self.cmd_args = [v for i, v in enumerate(content_list) if i > 0]
    
    def set_message(self, message: str) -> None:
        self.message = message

        content_list = self.message.content.split()
        if len(content_list) > 0:
            self.cmd_main = content_list[0]
            self.cmd_args = [v for i, v in enumerate(content_list) if i > 0]

    # Slightly more useful helper methods
    def command_name(self, name: str) -> str:
        return f"{self.prefix}{name}"
    
    # The coroutine decorator for commands
    async def command(self, command_func: callable) -> None:
        if self.cmd_main == self.command_name(command_func.__name__):
            try:
                await command_func(self.message, *self.cmd_args)
            except TypeError:
                pass


class ContextHandler:
    """An implementation of CommandHandler using ctx instead of messages"""
    def __init__(self, prefix='', ctx=None):
        self.prefix = prefix
        self.context = ctx
    
    def set_context(self, ctx) -> None:
        self.context = ctx

    # Slightly more useful helper methods
    def command_name(self, name: str) -> str:
        return f"{self.prefix}{name}"
    
    # The coroutine decorator lol
    async def command(self, command_func: callable) -> None:
        if self.context.cmd_main == self.command_name(command_func.__name__):

            try:
                await command_func(self.context, *self.context.cmd_args)
            except TypeError:
                pass

            # await command_func(self.context, *self.context.cmd_args)
    
    async def execute(self, commands) -> None:
        for function in inspect.getmembers(commands, inspect.isfunction):
            await self.command(function[1])
