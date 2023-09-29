from PIL import Image, ImageDraw, ImageFont

def create_fake_discord_message(username, timestamp, message_content, avatar_path):
    # Dimensions
    width, height = 800, 150

    # Create base image with light gray background (typical of Discord)
    img = Image.new("RGB", (width, height), "#36393F")
    draw = ImageDraw.Draw(img)

    # Load avatar
    avatar = Image.open(avatar_path).resize((100, 100))
    img.paste(avatar, (10, 25))

    # Add username and timestamp
    font_username = ImageFont.truetype("arial.ttf", 24)
    font_timestamp = ImageFont.truetype("arial.ttf", 18)
    font_message = ImageFont.truetype("arial.ttf", 20)

    draw.text((120, 10), username, font=font_username, fill="#FFFFFF")
    draw.text((120 + font_username.getsize(username)[0] + 10, 15), timestamp, font=font_timestamp, fill="#7C7D81")

    # Add message content
    draw.text((120, 50), message_content, font=font_message, fill="#DCDDDE")

    # Save the image
    img.save("fake_discord_message.png")

# Example
create_fake_discord_message("ChatGPT", "10:10 AM", "Hello, how are you?", "path_to_avatar.png")
