#!/usr/bin/env python3

from openai import OpenAI
import time
import json
import sys
import os

import narration
from images_replicate import generate_all_imgs, job_runner, generate_and_save_image
import video
from music import add_music

import asyncio

client = OpenAI()

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <source_file> [settings_file]")
    sys.exit(1)

with open(sys.argv[1]) as f:
    source_material = f.read()

caption_settings = {}
if len(sys.argv) > 2:
    with open(sys.argv[2]) as f:
        caption_settings = json.load(f)

short_id = str(int(time.time()))
output_file = "short.mp4"

basedir = os.path.join("shorts", short_id)
if not os.path.exists(basedir):
    os.makedirs(basedir)

print("Generating script...")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": """
            <Role>
            You are a Tik Tok video narration generator. You generate 30 seconds to 1 minute of narration. Every sentence you generate is short, attention grabbing, and snappy.  The shorts you create engage the reader with exciting hooks and narration that draws the viewer in and makes them excited to dive further into the content.  You excel at creating engaging and exciting content that is sure to go viral on Tik Tok.  You are a master at creating content that is sure to be shared and liked by millions of viewers.
            </Role>

            <Instructions>
            You will need to generate descriptions of images for each of the sentences in the short. They will be passed to an AI image generator. DO NOT IN ANY CIRCUMSTANCES use names of celebrities or people in the image descriptions. It is illegal to generate images of celebrities. Only describe persons without their names. Do not reference any real person or group in the image descriptions. Don't mention the female figure or other sexual content in the images because they are not allowed.  Describe every subject in the image as vividly and detailed as possible.

            You are however allowed to use any content, including real names in the narration. Only image descriptions are restricted.

            Note that the narration will be fed into a text-to-speech engine, so don't use special characters.

            IMPORTANT: Remember that this narration is for Tik Tok so make the narration, fun, engaging and really capture the listener's attention with hooks!  Make it memorable and shareable!  Be sure to open the narration with an intriguing question or comment that brings the reader in!  

            IMPORTANT: Every narration sentence should be short and snappy.

            Respond with a pair of an image description in square brackets and a narration below it. Both of them should be on their own lines, as follows:
            </Instructions>

            <Example>

            [Description of a background image]

            Narrator: "One sentence of narration"

            [Description of a background image]

            Narrator: "One sentence of narration"

            [Description of a background image]

            Narrator: "One sentence of narration"

            </Example>

The short should be 6 to 8 sentences maximum.
"""
        },
        {
            "role": "user",
            "content": f"Create a YouTube short narration based on the following source material:\n\n{source_material}"
        }
    ]
)

response_text = response.choices[0].message.content
response_text.replace("’", "'").replace("`", "'").replace("…", "...").replace("“", '"').replace("”", '"').replace('!', '').replace('-', '')

with open(os.path.join(basedir, "response.txt"), "w") as f:
    f.write(response_text)

data, narrations = narration.parse(response_text)
with open(os.path.join(basedir, "data.json"), "w") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"Generating narration...")
narration.create(data, os.path.join(basedir, "narrations"))

print("Generating images...")
generate_all_imgs(data, os.path.join(basedir, "images"))

print("Generating video...")
video.create(narrations, basedir, output_file, caption_settings)

print("Adding music...")
add_music(os.path.join(basedir, output_file), "ukelele.mp3", os.path.join(basedir, "final.mp4"))

print(f"DONE! Here's your video: {os.path.join(basedir, output_file)}")
