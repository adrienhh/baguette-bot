# baguette-bot
A Discord bot that can subsribe to subreddit listings and execute commands.

## Installation
### Dependencies
This project requires Python 3.6 or higher and the Discord library which uses the Discord API.

`pip3 install -U discord.py`

A Discord Developer account is required to acquire an API token.
An account can be created here:
https://discord.com/developers

### How to run the bot

Create a file called token.txt and paste the bot token.

Run MessageHandling.py in the command line using this command:

`python3 MessageHandling.py`  

## Functionalities
### Commands
The following commands can be executed by adding the command prefix (default: !) before the command name (ie: !ping)
| Command         | Arguments             | Description                                            |
|-----------------|-----------------------|--------------------------------------------------------|
| ping            | None                  | Bot will reply with pong                               |
| coinflip        | None                  | Bot will reply with heads or tails                     |
| choice          | choice1 choice2 ...   | Selects one of the choices given (whitespace separator)|
| supermute       | None                  | Mutes everyone currently in a voice channel            |
| unmute          | None                  | Unmutes everyone currently in a voice channel          |
| avatar          | @user                 | Returns the URL of the profile picture of the author if no arguments, otherwise returns the URL of the pinged user|
| purge           | n (@user)             | Deletes n number of previous messages sent by pinged user, otherwise removes n messages sent by any user (experimental)|
| die             | None                  | Terminates execution of the bot (bow owner only)       |

### Subscription to subreddits
The bot is able to keep watch on subreddits and post the listing it finds into discord channels.  
This requires a configuration file that specifies which subreddit to watch and in which channel from which guild (server) it should post what it finds.

A config file can be added with the -c (or --config) option when executing the code  
`python3 MessageHandling.py -c subreddit_config.json`

Here is an example of what the config file should look like:
```
{
    "guilds": [
        {
        "id": 660584552363222144,
        "postings": [
            {
                "channel_id": 874633283122234147,
                "has_custom_sorting": false,
                "subreddits": [
                    "Astronomy"
                ]
            },
            {
                "channel_id": 965501387053151066,
                "has_custom_sorting": true,
                "subreddits": [
                    {
                        "name": "Miata",
                        "sorting": "top"
                    },
                    {
                        "name": "RX7",
                        "sorting": "new"
                    }
                ]
            },
            ...
        ],
        },
        ...
    ],
    "delay": 4200
}
```

#### Parameters:  
"id" id of guild (server) in which the posts should be sent  
"channel_id": id of channel in which the posts should be sent  
"has_custom_sorting": indicates that the subreddits' listing can be different from "hot" (default value if not specified)  
"delay": amount of time to wait before checking a subreddit for new posts after posting in a channel  
 