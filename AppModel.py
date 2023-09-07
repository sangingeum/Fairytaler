from OpenAIUtils import *
from Character import *
from ImageCreator import *
import threading
from concurrent.futures import ThreadPoolExecutor
import pickle

# TODOS:
# TTS, 쓰레드 활용, 초상화, 아이템 이미지
# 게임 저장, 로드, 종료
# 게임 중간에 아이템 지급, 제거 이벤트
# 16k 컨텍스트를 넘어서도 내용이 이어지게
# 유저 인풋을 기다릴 때만 저장이 가능하게 하자

class AppModel:
    def __init__(self):
        self.protagonist = None
        self.universe = None
        self.messages = []
        self.main_text = ""
        self.waiting_user_input = False
        self.image_count = 0
        self.image_creator = ImageCreator()
        self.image_list_lock = threading.Lock()
        self.images = []
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
        self.new_game_text = """{}
        
[System] You received a(an) {}, {}. It can be equipped on your {}.

{}
"""

    def new_game(self, universe, name, gender, race, personality, background):
        print("new game")
        self.universe = universe
        with ThreadPoolExecutor(max_workers=2) as executor:
            item_future = executor.submit(create_equipable_item, self.equipment_generation_command.format(race, background, universe))
            universe_future = executor.submit(get_answer, self.fictional_universe_expander.format(self.universe))
        item = item_future.result()
        # create the protagonist
        character = Character(name=name, id=0, relationships=[], companions=[], consumables=[], equipments=[],
                              equipments_in_use={item["slot"]: item}, background=background, personality=personality,
                              race=race, gender=gender)
        self.protagonist = character
        self.universe = universe_future.result()
        # init message and get answer
        user_prompt = self.game_start_command.format(self.protagonist.name, self.universe, self.protagonist.describe())
        self.messages = []
        self.messages.append({"role": "user", "content": user_prompt})
        assistant_answer = chat_completion(self.messages)
        self.messages.append({"role": "assistant", "content": assistant_answer})

        self.waiting_user_input = True

        main_text = self.new_game_text.format(self.universe, item["name"], item["description"], item["slot"], assistant_answer)
        context_1 = self.image_prompt_generator.format(self.universe)
        context_2 = self.image_prompt_generator.format(assistant_answer)
        self.main_text = main_text
        return main_text, context_1, context_2

    def process_user_text(self, user_prompt):
        if self.waiting_user_input:
            self.main_text += "\n" + user_prompt + "\n"
            self.waiting_user_input = False
            self.messages.append({"role": "user", "content": user_prompt})
            assistant_answer = chat_completion(self.messages)
            self.messages.append({"role": "assistant", "content": assistant_answer})
            self.main_text += "\n" + assistant_answer + "\n"
            image_thread = threading.Thread(target=self.create_image_and_append, args=(assistant_answer,))
            image_thread.start()
            self.waiting_user_input = True
            return assistant_answer
        return None

    def create_image_and_append(self, context):
        image_prompt = create_prompt(self.image_prompt_generator.format(context))
        image = self.image_creator.create(image_prompt["prompt"], image_prompt["negative_prompt"])
        with self.image_list_lock:
            self.images.append(image)
        return image

    def save(self, path):
        try:
            if self.waiting_user_input:
                print("Saving [" + path + "]")
                with open(path, 'wb') as file:
                    pickle.dump(self.protagonist, file)
                    pickle.dump(self.universe, file)
                    pickle.dump(self.messages, file)
                    pickle.dump(self.main_text, file)
                    pickle.dump(self.waiting_user_input, file)
                    pickle.dump(self.image_count, file)
                    pickle.dump(self.images, file)
                print("Saving Complete")
                return True
            return False
        except:
            return False

    def load(self, path):
        try:
            print("Loading [" + path + "]")
            with open(path, 'rb') as file:
                self.protagonist = pickle.load(file)
                self.universe = pickle.load(file)
                self.messages = pickle.load(file)
                self.main_text = pickle.load(file)
                self.waiting_user_input = pickle.load(file)
                self.image_count = pickle.load(file)
                self.images = pickle.load(file)
            self.image_creator.change_image_count(self.image_count)
            print("Loading Complete")
            return True
        except:
            return False

    def exit(self):
        print("exit")
        exit()