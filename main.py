#!/usr/bin/env python
from collections import deque
import os
from PIL import Image
import requests
import sys
import telepot
import time

handled_updates = []

try:
    BOT_TOKEN = os.environ['BOT_TOKEN']
except KeyError:
    BOT_TOKEN = sys.argv[1]

endpoint = f'https://api.telegram.org/bot{BOT_TOKEN}'
file_endpoint = f'https://api.telegram.org/file/bot{BOT_TOKEN}'

def resize_image(path):
    img = Image.open(path)
    ratio = 512/max(img.size)
    new_size = (int(img.size[0]*ratio), int(img.size[1]*ratio))
    img = img.resize(new_size, Image.NEAREST)
    img.save(path + ".png", "png")
    return path + ".png"

def chat_handler(msg):
    msg_type, chat_type, chat_id = telepot.glance(msg)

    # Handle compressed/uncompressed images
    if msg_type == "document":
        print(msg["document"]["mime_type"])
        if msg["document"]["mime_type"] in ["image/png", "image/jpeg"]:
            file_id = msg["document"]["file_id"]
        else:
            return
    elif msg_type == "photo":
        print(msg["photo"][0])
        file_id = msg["photo"][0]["file_id"]
    else:
        return

    file_path = "downloads/" + bot.getFile(file_id)["file_path"].split("/")[1]

    # Download file
    bot.download_file(file_id, file_path)

    # Resize and send file
    new_file_path = resize_image(file_path)
    with open(new_file_path, "rb") as f:
        bot.sendDocument(chat_id, f)

    # Clean up working directory
    os.remove(file_path)
    os.remove(new_file_path)

if __name__ == "__main__":
    #make our bot and feed it the tokenhend
    bot = telepot.Bot(BOT_TOKEN)

    #fetch messages and keep script looped
    bot.message_loop({'chat' : chat_handler},
                      run_forever="Bot Running...")

