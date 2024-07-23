#!/usr/bin/env python3

from openai import OpenAI
import time
import json
import sys
import os

import narration
import images
import images_parallel
import video

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
output_file = "short.avi"

basedir = os.path.join("shorts", short_id)
if not os.path.exists(basedir):
    os.makedirs(basedir)

print("Generating script...")

response_text = """
[A cartoon soccer player juggling multiple soccer balls, looking exhausted]
Narrator: "Yo soccer fans! Ever feel like you need a vacation? Well, pro players are saying 'same' to FIFA!"
[Split screen: Soccer calendar packed with games vs. a tiny sliver of free time]
Narrator: "FIFA's pumping up the Club World Cup to 32 teams, but players are crying foul, saying they're more burnt out than your dad's BBQ!"
[Soccer player running on a hamster wheel, with another player relaxing on a beach chair]
Narrator: "Get this: 20-year-old Jude Bellingham's already played five times more than Beckham did at his age. Talk about hustle culture gone wild!"
[A soccer player lying on a therapist's couch, surrounded by thought bubbles of soccer balls]
Narrator: "It's not just bodies taking a hit - 43 percent of players are feeling the mental strain. Even soccer stars need their beauty sleep!"
[Soccer player sitting on a bench, looking sad, with angry fans in the background]
Narrator: "Fans are noticing too. Messi's been benching himself, and let's just say the crowd ain't happy!"
[A smartphone displaying the Morning Brew logo and newsletter]
Narrator: "For more juicy stories that'll kickstart your day, subscribe to Morning Brew!"
"""
response_text.replace("’", "'").replace("`", "'").replace("…", "...").replace("“", '"').replace("”", '"')

with open(os.path.join(basedir, "response.txt"), "w") as f:
    f.write(response_text)

data, narrations = narration.parse(response_text)
with open(os.path.join(basedir, "data.json"), "w") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"Generating narration...")
narration.create(data, os.path.join(basedir, "narrations"))

print("Generating images...")
images.create_from_data(data, os.path.join(basedir, "images"))

print("Generating video...")
video.create(narrations, basedir, output_file, caption_settings)

print(f"DONE! Here's your video: {os.path.join(basedir, output_file)}")
