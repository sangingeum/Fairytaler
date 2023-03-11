from Character import *
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

        for character_data in data_from_file[self.field_names[0]]:
            self.characters.append(Character(character_data["name"],
                                        character_data["id"],
                                        character_data["relationships"],
                                        character_data["items"],
                                        character_data["background"],
                                        character_data["personality"],
                                        character_data["race"]
                                        ))
        self.items = data_from_file[self.field_names[1]]
        self.backgrounds = data_from_file[self.field_names[2]]
        self.personalities = data_from_file[self.field_names[3]]
        self.races = data_from_file[self.field_names[4]]
        self.incidents = data_from_file[self.field_names[5]]

    def create_character(self):
        pass
    def create_item(self):
        pass
    def random_sample(self):
        pass
