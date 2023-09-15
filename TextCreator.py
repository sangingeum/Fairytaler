import json
import os
import openai


class TextCreator:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo-16k" # ["gpt-4", "gpt-3.5-turbo"]

    def chat_completion_with_string(self, user_prompt, system_prompt=None, return_token=False):
        messages = []
        if system_prompt is not None:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        return self.chat_completion_with_message(messages=messages, return_token=return_token)

    def chat_completion_with_message(self, messages, return_token=False):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        answer = response["choices"][0]["message"]["content"]
        if return_token:
            return answer, response['usage']['total_tokens']
        return answer

    def create_image_prompt(self, prompt="Create an image that depicts a cyberpunk city"):
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
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]
        function_args = json.loads(response_message["function_call"]["arguments"])
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
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]
        function_args = json.loads(response_message["function_call"]["arguments"])
        return function_args

    # need = "is a warrior", "is undead" 등 다양하게 사용 가능
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
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]
        function_args = json.loads(response_message["function_call"]["arguments"])
        return function_args
