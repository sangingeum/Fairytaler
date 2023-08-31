
from openai_utils import *
class Character:
    def __init__(self, name, id, relationships, companions, consumables, equipments, equipments_in_use, background,
                 personality, race, gender, status="Normal"):
        self.name = name
        self.id = id
        self.relationships = relationships
        self.companions = companions
        self.consumables = consumables
        self.equipments = equipments
        self.equipments_in_use = equipments_in_use
        self.background = background
        self.personality = personality
        self.race = race
        # "male" for male , "female" for female, "none" for None
        self.gender = gender
        self.status = status
        self.description = None
        self.changed = False

    def describe(self):
        if (not self.changed) and (self.description is not None):
            return self.description
        summary = """
Information about {}
gender: {}
race: {}
personality: {}
background: {}
equipments_in_use: {}
companions: {}
relationships: {}
status: {}
        """.format(self.name, self.gender, self.race, self.personality, self.background
                ,[self.equipments_in_use[key] for key in self.equipments_in_use], self.companions, self.relationships, self.status)

        return summary

    def to_dict(self):
        character_dict = {
            "race": self.race,
            "name": self.name,
            "gender": self.gender,
            "personality": self.personality,
            "status": self.status,
            "relationships": self.relationships,
            "companions": self.companions,
            "consumables": self.consumables,
            "equipments": self.equipments,
            "equipments_in_use": self.equipments_in_use,
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