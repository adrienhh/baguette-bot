# baguette-bot
A Discord bot that can subsribe to subreddit listings and execute commands.

## Commands
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

