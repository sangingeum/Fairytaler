import json
import os
from openai import OpenAI
import tiktoken

class TextCreator:
    def __init__(self, model="gpt-3.5-turbo-16k"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model #["gpt-4", "gpt-3.5-turbo"]
        self.encoder = tiktoken.encoding_for_model(model)

    def count_token(self, text : str) -> int:
        return len(self.encoder.encode(text))

    def chat_completion_with_string(self, user_prompt, system_prompt=None, return_token=False) -> str:
        messages = []
        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        return self.chat_completion_with_message(messages=messages, return_token=return_token)

    def chat_completion_with_message(self, messages, return_token=False) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        content = completion.choices[0].message.content
        if return_token:
            return content, completion.usage.total_tokens
        return content

    def create_image_prompt(self, prompt="Create an image that depicts a cyberpunk city", temperature=0.2):
        messages = [{"role": "user", "content": prompt}]
        functions = [
            {
                "name": "draw_image",
                "description": """Text-to-image generation function
    The prompt consists of keywords, which are descriptive adjectives or nouns to add depth and flavor to the resulting image.
    The negative_prompt consists of keywords that you don't want included in the image.
    For example, if the prompt is "cat swimming in day time", you could add "day" as a Keyword and "night" or "dark" as a negative_prompt.
    Keywords are separated by commas.
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
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
            temperature=temperature
        )
        response_message = completion.choices[0].message
        function_args = json.loads(response_message.function_call.arguments)
        return function_args

    def create_consumable_item(self,
            prompt="Create a single use item from the D&D universe considering that the player wants healing."):
        messages = [{"role": "user", "content": prompt}]
        functions = [
            {
                "name": "create_single_use_item",
                "description": "Create a single use item that have the given properties",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the item to be created",
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of the item to be created"
                        },
                    },
                    "required": ["name", "description"],
                },
            }
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = completion.choices[0].message
        function_args = json.loads(response_message.function_call.arguments)
        return function_args

    def create_equipable_item(self,
            prompt="Create an equipable item from the D&D universe considering that the player is a wizard."):
        messages = [{"role": "user", "content": prompt}]
        functions = [
            {
                "name": "create_equipable_item",
                "description": "Create an equipable item that matches the given properties."
                               "The item should not be single-use. It can be used multiple times.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the item to be created",
                        },
                        "slot": {
                            "type": "string",
                            "description": "The part where equipment can be worn or attached",
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of the item to be created"
                        },
                    },
                    "required": ["name", "slot", "description"],
                },
            }
        ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = completion.choices[0].message
        function_args = json.loads(response_message.function_call.arguments)
        return function_args


if __name__ == "__main__":
    # test TextCreator
    creator = TextCreator()
    response = creator.chat_completion_with_string("Good morning")
    print(response)
    response = creator.create_image_prompt()
    print(response)