import textwrap

import aiohttp
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

with open('token.txt', 'r') as file:
    TOKEN = file.readline().strip()

GUILD_ID = 1154768347481772092
REACTION_THRESHOLD = 10
REACTION_EMOJI = '💀'  # Skull emoji

intents = discord.Intents.all()  # Enables all intents.

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == REACTION_EMOJI:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if sum([react.count for react in message.reactions if react.emoji == REACTION_EMOJI]) == REACTION_THRESHOLD:

            for guild in bot.guilds:
                target_channel = discord.utils.get(guild.text_channels, name="😭-insane-sentences")
                if target_channel:  # break out of the loop once the channel is found
                    break

            if target_channel:
                # Get the timestamp
                timestamp = message.created_at.strftime('%Y-%m-%d %I:%M %p')

                avatar_url = str(message.author.avatar.url)
                avatar_path = "avatar.png"
                # Save the avatar locally to be used in the fake discord message
                async with aiohttp.ClientSession() as session:
                    async with session.get(avatar_url) as resp:
                        if resp.status == 200:
                            with open(avatar_path, 'wb') as f:
                                f.write(await resp.read())

                # Create fake Discord message as an image
                timestamp = message.created_at.strftime('%Y-%m-%d %I:%M %p')

                img = create_fake_discord_message(message.author.name, timestamp, message.content, avatar_path)

                # Save the image
                img_path = "message_image.png"
                img.save(img_path)

                # Send the saved image to the target channel
                await target_channel.send(file=discord.File(img_path))

                # Send a follow-up message
                await target_channel.send(f"<@{message.author.id}>")

                # Cleanup: remove saved images
                import os
                os.remove(img_path)
                os.remove(avatar_path)



def create_fake_discord_message(username, timestamp, message_content, avatar_path):
    width = 800
    padding = 20

    font_message = ImageFont.truetype("ggsans.ttf", 26)
    wrapped_text = textwrap.fill(message_content, width=60)
    lines = wrapped_text.split('\n')

    # Adjust height based on number of lines and font size
    per_line_height = font_message.getsize('A')[1] + 5  # using 'A' as a representative character
    dynamic_height = (len(lines) + 3) * per_line_height  # +3 for username, timestamp, and some spacing

    # Now use dynamic_height as your height when creating the image
    img = Image.new("RGB", (width+ 20, dynamic_height+ 15), "#36393F")
    draw = ImageDraw.Draw(img)

    # Load avatar and make it circular
    avatar_size = 100
    avatar = Image.open(avatar_path).resize((avatar_size, avatar_size))
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    circular_avatar = Image.composite(avatar, Image.new("RGBA", avatar.size, (0, 0, 0, 0)), mask)
    img.paste(circular_avatar, (10, 25), mask)


    # Add username and timestamp
    font_username = ImageFont.truetype("ggsansbold.ttf", 26)
    font_timestamp = ImageFont.truetype("ggsansmedium.ttf", 20)
    font_message = ImageFont.truetype("ggsans.ttf", 26)

    draw.text((120, 10), username, font=font_username, fill="#FFFFFF")
    draw.text((120 + font_username.getsize(username)[0] + 10, 15), timestamp, font=font_timestamp, fill="#a4a5ab")

    # Add message content with wrapped text
    y_text = 60
    for line in lines:
        draw.text((140, y_text), line, font=font_message, fill="#DCDDDE")  # Moved text a bit right to accommodate avatar
        y_text += font_message.getsize(line)[1] + 5

    return img


bot.run(TOKEN)
