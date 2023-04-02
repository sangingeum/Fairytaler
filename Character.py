
from openai_utils import *
class Character:
    def __init__(self, name, id, relationships, companions, items, background, personality, race, gender):
        self.name = name
        self.id = id
        self.relationships = relationships
        self.companions = companions
        self.items = items
        self.background = background
        self.personality = personality
        self.race = race
        # "male" for male , "female" for female, "none" for None
        self.gender = gender
        self.description = None
        self.changed = False

    def describe(self):
        if (not self.changed) and (self.description is not None):
            return self.description

        system_prompt = "You are a helpful assistant."
        user_prompt = "Summarize information about me."\
                                            "\nname:{}"\
                                            "\nrelationships:{}"\
                                            "\ncompanions:{}"\
                                            "\nitems:{}"\
                                            "\nbackground:{}"\
                                            "\npersonality:{}"\
                                            "\nrace:{}"\
                                            "\ngender:{}".format(self.name, self.relationships,
                                                               self.companions,
                                                               self.items, self.background,
                                                               self.personality, self.race,
                                                                 self.gender)

        summary = get_answer(system_prompt, user_prompt)
        self.description = summary
        return summary

    def to_dict(self):
        character_dict = {
            "race": self.race,
            "name": self.name,
            "gender": self.gender,
            "personality": self.personality,
            "relationships": self.relationships,
            "companions": self.companions,
            "items": self.items,
            "background": self.background
        }
        return character_dict

    def describe_relationship(self, target_character):
        target_name = target_character.name
        to_target_relationship = self.relationships.get(target_name)
        if to_target_relationship is None:
            self.relationships[target_name] = "first encounter"
        from_target_relationship = target_character.relationships.get(self.name)
        if from_target_relationship is None:
            target_character.relationships[self.name] = "first encounter"
        description = "\nRelationship:" \
                      "\nFrom {} to {}: {}" \
                      "\nFrom {} to {}: {}".format(self.name, target_name, self.relationships[target_name],
                                                   target_name, self.name, target_character.relationships[self.name])
        return description