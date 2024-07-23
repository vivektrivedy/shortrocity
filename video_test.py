from openai import OpenAI
import time
import json
import sys
import os

import narration
import images
import images_parallel
import video

basedir = os.path.join("shorts", '1721098153')
narrations = 
output_file = 
caption_settings = 'settings.json'
video.create(narrations, basedir, output_file, caption_settings)