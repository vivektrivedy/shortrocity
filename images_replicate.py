import asyncio
import aiohttp
import aiofiles
import os
import replicate
import time


def generate_all_imgs(script_json, output_dir):
    """wrapper function to parse script for all image prompts and async generate all images"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    prompts = []
    for element in script_json:
        if element["type"] == "image":
            prompts.append(element["description"])

    asyncio.run(job_runner(prompts, output_dir))



async def generate_and_save_image(session, prompt, image_number, output_dir):
    """async function to generate and save single image"""
    # Initialize the Replicate client
    client = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

    input = {
    "prompt": f"{prompt}",
    "aspect_ratio": "9:16",
    "steps": 28,
    'output_format':'webp'
    }   
    
    # Run the model
    output = await client.async_run(
        "stability-ai/stable-diffusion-3",
        input=input
    )

    # Get the image URL from the output
    image_url = output[0]

    # Download the image
    async with session.get(image_url) as response:
        if response.status == 200:
            image_name = f"image_{image_number}.webp"
            filename = os.path.join(output_dir, image_name)
            async with aiofiles.open(filename, mode='wb') as f:
                await f.write(await response.read())
            print(f"Saved {filename}")
        else:
            print(f"Failed to download image for prompt: {prompt}")



async def job_runner(prompts, output_dir):
    """async function create async task for each prompt and then run everything via async gather"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, prompt in enumerate(prompts, start=1):
            task = asyncio.create_task(generate_and_save_image(session, prompt, index, output_dir))
            tasks.append(task)
        
        await asyncio.gather(*tasks)



if __name__ == "__main__":
    prompts = [
        "A serene lake at sunset",
        "A bustling cityscape at night",
        "A field of wildflowers in bloom",
        # Add more prompts as needed
    ]
    start = time.time()
    asyncio.run(job_runner(prompts))
    end = time.time()
    print(f"Time taken: {end - start} seconds")