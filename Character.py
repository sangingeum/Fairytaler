import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

class Character:
    def __init__(self, name, id, relationships, companions, items, background, personality, race):
        self.name = name
        self.id = id
        self.relationships = relationships
        self.companions = companions
        self.items = items
        self.background = background
        self.personality = personality
        self.race = race
        self.description = None
        self.changed = False

    def describe(self):
        if (not self.changed) and (self.description is not None):
            return self.description

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Summarize information about me."
                                            "\nname:{}"
                                            "\nrelationships:{}"
                                            "\ncompanions:{}"
                                            "\nitems:{}"
                                            "\nbackground:{}"
                                            "\npersonality:{}"
                                            "\nrace:{}".format(self.name, self.relationships,
                                                               self.companions,
                                                               self.items, self.background,
                                                               self.personality, self.race)
                }
            ]
        )
        summary = response["choices"][0]["message"]["content"]
        self.description = summary
        # print(response["choices"][0]["message"]["content"])
        return summary

    def to_dict(self):
        character_dict = {
            "name": self.name,
            "relationships": self.relationships,
            "companions": self.companions,
            "items": self.items,
            "background": self.background,
            "personality": self.personality,
            "race": self.race
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