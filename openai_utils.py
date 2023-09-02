import openai
import json
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_answer(user_prompt, system_prompt=None, return_token=False):
    messages = []
    if system_prompt is not None:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    return chat_completion(messages=messages, return_token=return_token)
def chat_completion(messages, return_token=False):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",  # ["gpt-4", "gpt-3.5-turbo"]
        messages=messages
    )
    answer = response["choices"][0]["message"]["content"]
    if return_token:
        return answer, response['usage']['total_tokens']
    return answer

def create_prompt(universe="cyberpunk"):
    prompt = """Create an image that depicts this: 
    "{}"
    """.format(universe)
    messages = [{"role": "user", "content": prompt}]
    functions = [
        {
            "name": "draw_image",
            "description": """Text-to-image generation function
The prompt consists of keywords, which are descriptive adjectives or nouns to add depth and flavor.
The negative_prompt are the descriptive adjectives or keywords that you don't want included in the image.
For example, if the prompt is "cat swimming in day time", you could add "day" as a Keyword and "night" or "dark" as a negative_prompt.
Keywords are separated by commas.
Please follow this exact pattern and do not make up your own.
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to guide the image generation",
                    },
                    "negative_prompt": {
                        "type": "string",
                        "description": "The prompt not to guide the image generation",
                    },
                },
                "required": ["prompt", "negative_prompt"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    function_args = json.loads(response_message["function_call"]["arguments"])
    return function_args