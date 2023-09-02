from Character import *
import random
import json
from OpenAIUtils import *

class ResourcePool:
    def __init__(self):
        self.characters = []
        self.consumables = []
        self.equipments = []
        self.backgrounds = []
        self.personalities = []
        self.races = []
        self.incidents = []
        self.field_names = ["character", "consumables", "equipments", "background", "personality", "race", "incident"]

    def load_resource(self, path=None):
        if path is None:
            path = "resource.json"
        with open(path, "r") as f:
            data_from_file = json.load(f)

        self.characters = [Character(character_data["name"],
                                     id,
                                     character_data["relationships"],
                                     character_data["companions"],
                                     character_data["consumables"],
                                     character_data["equipments"],
                                     character_data["background"],
                                     character_data["personality"],
                                     character_data["race"],
                                     character_data["gender"]
                                     )
                           for id, character_data in enumerate(data_from_file[self.field_names[0]])]
        self.consumables = data_from_file[self.field_names[1]]
        self.equipments = data_from_file[self.field_names[2]]
        self.backgrounds = data_from_file[self.field_names[3]]
        self.personalities = data_from_file[self.field_names[4]]
        self.races = data_from_file[self.field_names[5]]
        self.incidents = data_from_file[self.field_names[6]]

    def save_resource(self, path=None):
        if path is None:
            path = "saved_resource.json"
        data_to_file = {
            self.field_names[0]: [character.to_dict() for character in self.characters],
            self.field_names[1]: self.consumables,
            self.field_names[2]: self.equipments,
            self.field_names[3]: self.backgrounds,
            self.field_names[4]: self.personalities,
            self.field_names[5]: self.races,
            self.field_names[6]: self.incidents,
        }
        with open(path, "w") as f:
            json.dump(data_to_file, f)

    def create_character(self):
        pass

    # need = "is a rogue", "is paralyzed" 등 다양하게 사용 가능
    def create_consumable_item(self,
            prompt="Create a consumable item from the D&D universe considering that the player wants healing."):
        messages = [{"role": "user", "content": prompt}]
        functions = [
            {
                "name": "create_consumable_item",
                "description": "Create a consumable item that matches the given properties",
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
            model="gpt-3.5-turbo-16k",
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]
        function_args = json.loads(response_message["function_call"]["arguments"])
        self.consumables.append(function_args)
        return function_args

    # need = "is a warrior", "is undead" 등 다양하게 사용 가능
    def create_equipable_item(self,
            prompt="Create an equipable item from the D&D universe considering that the player is a wizard."):

        messages = [{"role": "user", "content": prompt}]
        functions = [
            {
                "name": "create_equipable_item",
                "description": "Create an item that matches the given properties",
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
            model="gpt-3.5-turbo-16k",
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]
        function_args = json.loads(response_message["function_call"]["arguments"])
        self.equipments.append(function_args)
        return function_args



