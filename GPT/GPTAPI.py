import json
import subprocess
import asyncio
import tiktoken
import openai

# Loading configuration from config.json
with open("../config.json") as config_file:
    json_config = json.load(config_file)

# OpenAIApi API key from config.json
openai.api_key = json_config["openai"]["api_key"]

async def generate_completion(chunk):
    prompt = json_config["gpt"]["prompt"] + chunk
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return res["choices"][0]["message"]["content"]
    except Exception as error:
        error_message = getattr(error.response, "data", {}).get("error", {}).get("message", str(error))
        print(f"GPT-3.5 Error: {error_message}")
        exit(1)

async def main():
    with open(json_config["gpt"]["input_file"], "r") as input_file:
        input_text = input_file.read()

    chunk_size = json_config["gpt"]["chunk_size"]

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(input_text)

    num_tokens = len(tokens)
    chunks = [tokens[i : i + chunk_size] for i in range(0, num_tokens, chunk_size)]

    promises = [generate_completion(encoding.decode(chunk)) for chunk in chunks]
    outputs = await asyncio.gather(*promises)

    with open(json_config["gpt"]["output_file"], "a", encoding="utf-8") as output_file:
        for output in outputs:
            output_file.write(output)

asyncio.run(main())
