from ResourcePool import *
from ImageCreator import *

# TODOS:
# TTS, 쓰레드 활용, 초상화, 아이템 이미지
# 게임 저장, 로드, 종료
# 게임 중간에 아이템 지급, 제거 이벤트
# 16k 컨텍스트를 넘어서도 내용이 이어지게

class StoryManager:
    def __init__(self):
        self.story = ""
        self.resource_pool = ResourcePool()
        self.resource_pool.load_resource()
        self.image_creator = ImageCreator()
        self.protagonist = None
        self.universe = None

        # prompts
        self.fictional_universe_expander = """I want you to act as a novel writer.
The fictional universe of the story is like this : {}
Introduce the fictional universe while not mentioning any named characters.
To enhance immersion, avoid mentioning readers and the term 'fictional universe'.
"""
        self.image_prompt_generator = """Make an illustration for this text:
"{}" 
"""
        self.game_start_command = """I want you to act as the GM of a TRPG game based on the universe and characters written below.
When a character attempts critical actions such as attacks, escapes, and evades, you need to determine the success or failure of the attempt by rolling a 1d20 die.
A roll of 10 or above indicates success, while anything below 10 is a failure.
Equipments, companions, relationships, and status of {0} can change during the playthrough. It's your responsibility to update them correctly.
To enhance immersion, avoid mentioning the term 'fictional universe'.
The GM do not decide {0}'s action. You can ask {0} when you need to decide his/her action. 
I'll play as {0}.
Start by introducing a plausible event that happens to {0}.

Fictional universe:
{1}

Protagonist information:
{2}
"""

    # basic operations
    def save(self, path):
        pass
    def load(self, path):
        pass
    def start(self):
        if self.protagonist is None:
            self.init()
        self.tell_story()
    def end(self):
        pass

    def ask_and_confirm(self, question):
        while True:
            user_input = input(question + "\n")
            yes_or_no = input("Do you want to change your answer? (y/n):")
            if yes_or_no.lower() == "y":
                continue
            break
        return user_input

    def init(self):
        # Set the universe
        universe = self.ask_and_confirm("Describe the fictional universe you want to explore.")
        self.universe = universe
        # Set the protagonist name
        name = self.ask_and_confirm("Write the name of the protagonist.")
        # Set the protagonist gender
        gender = self.ask_and_confirm("Write the gender of the protagonist. (male/female)")
        # Set the protagonist race
        race = self.ask_and_confirm("What is the race of the protagonist?")
        # Set the protagonist personality
        personality = self.ask_and_confirm("Describe the personality of the protagonist.")
        # Set the protagonist background
        background = self.ask_and_confirm("Describe the background of the protagonist.")

        # Create an equipable item
        print("We will give you an equipment as a gift.")
        item = self.resource_pool.create_equipable_item("Create an equipable item from the D&D universe considering that the player is (a/an)"+ race + "and the universe the player is in is like this: "+ universe+".")
        print("You received a(an) {}, {}, which can be put on your {}.".format(item["name"], item["description"], item["slot"]))

        # Create the protagonist
        character = Character(name=name, id=0, relationships=[], companions=[], consumables=[], equipments=[],
                  equipments_in_use={item["slot"]: item}, background=background, personality=personality, race=race,
                  gender=gender)
        self.protagonist = character

        # Replace the existing universe
        prompt = self.fictional_universe_expander.format(self.universe)
        self.universe = get_answer(prompt)
        # print the universe description
        print(self.universe)
        # Create initial image
        image_prompt = create_prompt(self.image_prompt_generator.format(self.universe))
        self.image_creator.create(image_prompt["prompt"], image_prompt["negative_prompt"])

    def tell_story(self):
        user_prompt = self.game_start_command.format(self.protagonist.name, self.universe, self.protagonist.describe())
        messages = []
        while True:
            messages.append({"role": "user", "content": user_prompt})
            assistant_answer = chat_completion(messages)
            messages.append({"role": "assistant", "content": assistant_answer})
            #print(user_prompt)
            print(assistant_answer)
            # Create image
            image_prompt = create_prompt(self.image_prompt_generator.format(assistant_answer))
            self.image_creator.create(image_prompt["prompt"], image_prompt["negative_prompt"])

            user_prompt = input(":")




