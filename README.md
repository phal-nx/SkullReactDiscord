# Discord Reaction Image Bot

A Discord bot that listens for reactions on messages. When a certain reaction threshold is reached on a message, the bot takes the message and turns it into an image to post in a specific channel.

## Features:
- Listens for a specific reaction emoji.
- Converts the content of the message into an image.
- Supports converting attached images in the original message.
- Circular avatars in the fake Discord message.
- Resizes multiple attached images proportionally.
- Links back to the original message as a follow-up.

## Setup:
### Prerequisites:
- Python 3.x
- `discord.py` library with voice support (to provide the `intents` option).
- `textwrap`, `aiohttp`, and `PIL` libraries.

### Steps:
1. **Token File**: Save your bot token in a file named `token.txt`. This will keep your token secure and separate from your main code. The bot will read the token from this file.
2. **Dependencies**: Install the required libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```
### Configuration:
- TOKEN: Your bot token, read from the token.txt file.
- REACTION_THRESHOLD: The number of reactions a message needs to reach before being processed.
- REACTION_EMOJI: The specific emoji the bot should look for.

## How It Works:

When a message receives the specified number of reactions, the bot:

1. Checks if there are any attached images in the message.
2. Downloads the images and resizes them proportionally to fit within the message's width.
3. Converts the content of the message and its attached images into one combined image.
4. Sends the image to a specified channel.
5. Sends a link back to the original message.
