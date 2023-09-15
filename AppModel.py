import pickle
from concurrent.futures import ThreadPoolExecutor
from Character import *
from ImageCreator import *
from TextCreator import *
from MusicCreator import *
from scipy.io.wavfile import write as write_wav
import pygame
from PIL import Image

# TODOS:
# TTS, 쓰레드 활용, 초상화, 아이템 이미지
# 게임 중간에 아이템 지급, 제거 이벤트
# 16k 컨텍스트를 넘어서도 내용이 이어지게
# 상태표시(생성중, 대기중 등)
# 로고 만들기

class AppModel:
    def __init__(self):
        self.protagonist = None
        self.universe = None
        self.messages = []
        self.main_text = ""
        self.waiting_user_input = False
        self.image_creator = ImageCreator()
        self.image_list_lock = threading.Lock()
        self.image_index = 0
        self.image_count = 0

        self.music_creator = MusicCreator()
        self.music_list_lock = threading.Lock()
        self.music_index = 0
        self.music_count = 0
        self.music_length = 0

        self.save_dir = None
        self.save_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "saves")

        self.text_creator = TextCreator()
        # pygame
        pygame.init()
        self.mixer = pygame.mixer.music
        self.MUSIC_END = pygame.USEREVENT + 1
        self.mixer.set_endevent(self.MUSIC_END)

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

{}"""
    def __del__(self):
        pygame.quit()

    def reset(self):
        self.protagonist = None
        self.universe = None
        self.messages = []
        self.main_text = ""
        self.waiting_user_input = False
        self.image_index = 0
        self.image_count = 0
        self.music_index = 0
        self.music_count = 0
        self.music_length = 0
        self.save_dir = None

    def new_game(self, universe, name, gender, race, personality, background, save_name):
        print("new game")
        self.reset()
        self.universe = universe
        self.save_dir = "saves/" + save_name + "/"
        os.makedirs("saves/" + save_name)

        with ThreadPoolExecutor(max_workers=2) as executor:
            item_future = executor.submit(self.text_creator.create_equipable_item,
                                          self.equipment_generation_command.format(race, background, universe))
            universe_future = executor.submit(self.text_creator.chat_completion_with_string,
                                              self.fictional_universe_expander.format(self.universe))
        item = item_future.result()
        # create the protagonist
        character = Character(name=name, id=0, relationships=[], companions=[], consumables=[], equipments=[],
                              equipments_in_use={item["slot"]: item}, background=background, personality=personality,
                              race=race, gender=gender)
        self.protagonist = character
        self.universe = universe_future.result()
        # init message and get answer
        user_prompt = self.game_start_command.format(self.protagonist.name, self.universe, self.protagonist.describe())
        self.messages.append({"role": "user", "content": user_prompt})
        assistant_answer = self.text_creator.chat_completion_with_message(self.messages)
        self.messages.append({"role": "assistant", "content": assistant_answer})
        self.waiting_user_input = True
        main_text = self.new_game_text.format(self.universe, item["name"], item["description"], item["slot"],
                                              assistant_answer)
        context_1 = self.image_prompt_generator.format(self.universe)
        context_2 = self.image_prompt_generator.format(assistant_answer)
        self.main_text = main_text
        return main_text, context_1, context_2

    def process_user_text(self, user_prompt):
        if self.waiting_user_input:
            self.main_text += "\n\n[{}] ".format(self.protagonist.name) + user_prompt
            self.waiting_user_input = False
            self.messages.append({"role": "user", "content": user_prompt})
            assistant_answer = self.text_creator.chat_completion_with_message(self.messages)
            self.messages.append({"role": "assistant", "content": assistant_answer})
            self.main_text += "\n\n" + assistant_answer
            self.waiting_user_input = True
            return assistant_answer
        return None

    def create_and_save_image(self, context):
        image_prompt = self.text_creator.create_image_prompt(self.image_prompt_generator.format(context))
        with self.image_list_lock:
            cur_count = self.image_count
            self.image_count += 1
        image = self.image_creator.create(image_prompt["prompt"], image_prompt["negative_prompt"])
        image.save(self.save_dir + f"{cur_count}.jpg")
        return cur_count

    def create_and_save_music(self, text):
        musics = self.music_creator.create(text)
        for music in musics:
            with self.music_list_lock:
                cur_count = self.music_count
                self.music_count += 1
            signal, rate = music
            write_wav(self.save_dir + f"{cur_count}.wav", rate=rate, data=signal)

    def get_prev_image(self):
        index = self.image_index - 1
        image = self.get_image(index)
        if image is not None:
            self.image_index = index
        return image

    def get_next_image(self):
        index = self.image_index + 1
        image = self.get_image(index)
        if image is not None:
            self.image_index = index
        return image

    def get_last_image(self):
        for index in range(self.image_count - 1, -1, -1):
            image = self.get_image(index)
            if image is not None:
                self.image_index = index
                return image
        return None

    def get_image(self, index:int):
        with self.image_list_lock:
            try:
                image = Image.open(self.save_dir + f"{index}.jpg")
                self.image_index = index
                return image
            except:
                return None

    def load_prev_music(self):
        index = self.music_index - 1
        return self.load_music(index), index

    def load_next_music(self):
        index = self.music_index + 1
        return self.load_music(index), index

    def load_last_music(self):
        if self.music_count > 0:
            for index in range(self.music_count - 1, -1, -1):
                if self.load_music(index):
                    return True, index
        return False, 0

    def load_first_music(self):
        return self.load_music(0), 0

    def load_music(self, index) -> bool:
        with self.music_list_lock:
            try:
                print("Loading music " + self.save_dir + f"{index}.wav")
                self.mixer.stop()
                # empty MUSIC_END event
                for _ in pygame.event.get():
                    pass
                self.mixer.load(self.save_dir + f"{index}.wav")
                self.music_length = pygame.mixer.Sound(self.save_dir + f"{index}.wav").get_length()
                self.music_index = index
                print("Loading complete")
                return True
            except:
                return False

    def play_music(self):
        try:
            if self.mixer.get_pos() == -1:
                self.mixer.play()
            else:
                if self.mixer.get_busy():
                    self.mixer.pause()
                else:
                    self.mixer.unpause()
        except:
            success, index = self.load_first_music()
            if success:
                self.play_music()
                return True, index
            else:
                print("no music detected")
        return False, ""

    def save(self):
        try:
            if self.waiting_user_input:
                path = self.save_dir + "game.sav"
                print("Saving [" + path + "]")
                with open(path, 'wb') as file:
                    pickle.dump(self.protagonist, file)
                    pickle.dump(self.universe, file)
                    pickle.dump(self.messages, file)
                    pickle.dump(self.main_text, file)
                    pickle.dump(self.waiting_user_input, file)
                    pickle.dump(self.image_index, file)
                    pickle.dump(self.image_count, file)
                    pickle.dump(self.music_index, file)
                    pickle.dump(self.music_count, file)
                    pickle.dump(self.music_length, file)
                    pickle.dump(self.save_dir, file)
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
                self.image_index = pickle.load(file)
                self.image_count = pickle.load(file)
                self.music_index = pickle.load(file)
                self.music_count = pickle.load(file)
                self.music_length = pickle.load(file)
                self.save_dir = pickle.load(file)
            print("Loading Complete")
            return True
        except:
            return False

    def exit(self):
        print("exit")
        exit()
