from OpenAIUtils import *
from Character import *
from ImageCreator import *
import threading
import pickle

# TODOS:
# TTS, 쓰레드 활용, 초상화, 아이템 이미지
# 게임 저장, 로드, 종료
# 게임 중간에 아이템 지급, 제거 이벤트
# 16k 컨텍스트를 넘어서도 내용이 이어지게

class AppModel:
    def __init__(self):
        self.image_creator = ImageCreator()
        self.protagonist = None
        self.universe = None
        self.messages = []
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
        self.equipment_generation_command = """Create an equipable item for a player whose race is {0} and background is {1}.
The universe the player is in is like this: 
{2}
"""
        self.consumable_generation_command = """Create a consumable item for a player whose race is {0} and background is {1}.
The universe the player is in is like this: 
{2}
"""

    # basic operations
    def save(self, path=None):
        if path is None:
            path = "saves/save0.pkl"
        print("Saving [" + path + "]")
        with open(path, 'wb') as file:
            pickle.dump(self.messages, file)
            pickle.dump(self.protagonist, file)
            pickle.dump(self.universe, file)
        print("Saving Complete")

    def load(self, path=None):
        if path is None:
            path = "saves/save0.pkl"
        print("Loading [" + path + "]")
        with open(path, 'wb') as file:
            self.messages = pickle.load(file)
            self.protagonist = pickle.load(file)
            self.universe = pickle.load(file)
        print("Loading Complete")
    def start(self):
        self.tell_story()

    def exit(self):
        exit()

    def new_game(self):
        self.init()
        self.start()

    def load_latest(self):
        self.load()

    def lobby_menu(self):
        print("What would you like to do?")
        print("1. new game")
        print("2. load")
        while True:
            user_input = input("Enter number(1~3):")
            if user_input in ["1", "2", "3"]:
                if user_input == "1":
                    self.new_game()
                    break
                elif user_input == "2":
                    self.load()
                elif user_input == "3":
                    self.exit()



    def in_game_menu(self):
        print("What would you like to do?")
        print("1. save")
        print("2. load")
        print("3. exit")
        print("4. go to lobby")
        print("5. go back to game")
        while True:
            user_input = input("Enter number(1~5):")
            if user_input in ["1", "2", "3", "4", "5"]:
                if user_input == "1":
                    self.save()
                elif user_input == "2":
                    self.load()
                elif user_input == "3":
                    self.exit()
                elif user_input == "4":
                    self.lobby_menu()
                elif user_input == "5":
                    pass
                break

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
        item = create_equipable_item(self.equipment_generation_command.format(race, background, universe))
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

        image_thread = threading.Thread(target=self.image_creator.create, args=(image_prompt["prompt"], image_prompt["negative_prompt"],))
        image_thread.start()
        #self.image_creator.create(image_prompt["prompt"], image_prompt["negative_prompt"])

    def tell_story(self):
        user_prompt = self.game_start_command.format(self.protagonist.name, self.universe, self.protagonist.describe())
        self.messages = []
        while True:
            self.messages.append({"role": "user", "content": user_prompt})
            assistant_answer = chat_completion(self.messages)
            self.messages.append({"role": "assistant", "content": assistant_answer})
            #print(user_prompt)
            print(assistant_answer)
            # Create image
            image_prompt = create_prompt(self.image_prompt_generator.format(assistant_answer))
            image_thread = threading.Thread(target=self.image_creator.create, args=(image_prompt["prompt"], image_prompt["negative_prompt"],))
            image_thread.start()
            #self.image_creator.create(image_prompt["prompt"], image_prompt["negative_prompt"])
            user_prompt = input(":")
            if user_prompt == "menu":
                self.main_menu()




