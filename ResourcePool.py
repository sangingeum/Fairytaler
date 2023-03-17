from Character import *
import random
from Item import *
import json


class ResourcePool:
    def __init__(self):
        self.characters = []
        self.items = []
        self.backgrounds = []
        self.personalities = []
        self.races = []
        self.incidents = []
        self.field_names = ["character", "item", "background", "personality", "race", "incident"]

    def load_resource(self, path=None):
        if path is None:
            path = "resource.json"
        with open(path, "r") as f:
            data_from_file = json.load(f)

        self.characters = [Character(character_data["name"],
                                     id,
                                     character_data["relationships"],
                                     character_data["companions"],
                                     character_data["items"],
                                     character_data["background"],
                                     character_data["personality"],
                                     character_data["race"]
                                     )
                           for id, character_data in enumerate(data_from_file[self.field_names[0]])]
        self.items = data_from_file[self.field_names[1]]
        self.backgrounds = data_from_file[self.field_names[2]]
        self.personalities = data_from_file[self.field_names[3]]
        self.races = data_from_file[self.field_names[4]]
        self.incidents = data_from_file[self.field_names[5]]

    def save_resource(self, path=None):
        if path is None:
            path = "saved_resource.json"
        data_to_file = {
            self.field_names[0]: [character.to_dict() for character in self.characters],
            self.field_names[1]: self.items,
            self.field_names[2]: self.backgrounds,
            self.field_names[3]: self.personalities,
            self.field_names[4]: self.races,
            self.field_names[5]: self.incidents,
        }
        with open(path, "w") as f:
            json.dump(data_to_file, f)

    def create_character(self):
        id = len(self.characters)
        item = random.choice(self.items)
        background = random.choice(self.backgrounds)
        personality = random.choice(self.personalities)
        race = random.choice(self.races)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content":
                            "Recommend me a name for this character."
                            "\nCharacter information:"
                            #"\nitme: {}" # don't make it affect the name.
                            "\nbackground: {}"
                            "\npersonality: {}"
                            "\nrace: {}"
                            "\nYou don't need to explain why you wrote the name."
                            "\nAnswer in a word.".format(item, background, personality, race)}
            ]
        )
        name = response["choices"][0]["message"]["content"].replace(".", "")
        character = Character(name, id, [], [], [item], background, personality, race)
        self.characters.append(character)
        #print(character.to_dict())

        return character

    def create_item(self):
        pass


