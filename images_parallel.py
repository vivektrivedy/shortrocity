#same as images.py but use ThreadPoolExecutor to parallelize the image generation process

from openai import OpenAI
import base64
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

client = OpenAI()

def create_from_data(data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    start = time.time()
    tasks = []
    for image_number, element in enumerate(data, start=1):
        if element["type"] != "image":
            continue
        image_name = f"image_{image_number}.webp"
        prompt = element["description"] + ". Vertical image, fully filling the canvas."
        output_file = os.path.join(output_dir, image_name)
        tasks.append((prompt, output_file))

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate, prompt, output_file) for prompt, output_file in tasks]
        for future in as_completed(futures):
            future.result()  # This will raise any exceptions that occurred during execution
    
    end = time.time()
    print(f"Generated {len(tasks)} images in {end - start:.2f} seconds")

def generate(prompt, output_file, size="1024x1792"):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        response_format="b64_json",
        n=1,
    )

    image_b64 = response.data[0].b64_json

    with open(output_file, "wb") as f:
        f.write(base64.b64decode(image_b64))

    return output_file  # Return the output file path for confirmation