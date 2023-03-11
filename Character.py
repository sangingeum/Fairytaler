import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

class Character:
    def __init__(self, name, id, relationships, items, background, personality, race):
        self.name = name
        self.id = id
        self.relationships = relationships
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
                                            "\nitems:{}"
                                            "\nbackground:{}"
                                            "\npersonality:{}"
                                            "\nrace:{}".format(self.name, self.relationships,
                                                               self.items, self.background,
                                                               self.personality, self.race)
                }
            ]
        )
        # print(response["choices"][0]["message"]["content"])
        return response["choices"][0]["message"]["content"]
