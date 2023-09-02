from ResourcePool import *
from ImageCreator import *


# TODOS:
# 이미지 생성, 쓰레드 활용

"""
게임 시작
1. 세계관 설정, 주인공 이름과 성별, 종족, 성격, 배경 설정
2. AI가 세계 묘사(그림, 텍스트)
3. 캐릭터 장비 확인
4. 캐릭터 초상화 생성

이야기 시작

이야기 묘사(그림, 텍스트) + 랜덤으로 아이템 추가/삭제 이벤트
{1} 묘사가 끝나면 플레이어 선택지 표시, 선택
선택지: [AI가 생성한 선택지], [사용자 지정 선택지], [아이템 사용], [저장], [로드], [종료]
-[AI가 생성한 선택지]: GPT가 현재 상황을 고려하여 선택지 생성
-- 주의: 가지고 있지 않은 아이템의 사용 금지, 디버프와 버프 고려
-[사용자 지정 선택지]: 사용자가 직접 선택지를 적어서 이야기를 진행함, 사용횟수가 무제한이 아님
-[아이템 사용]: 캐릭터의 인벤토리 리스트 표시, 숫자 입력으로 사용
-- 장비 아이템/소모품 차이 고려
-[저장]: save 폴더에 저장. 자동, 수동 파일 이름 설정. 이름 겹치면 덮어 씌울지 결정
-[로드]: save 폴더 스캔해서 불러올 수 있는 파일 표시. 사용자가 선택하면 불러와짐
-[종료]: 게임 종료

선택지 선택 후:
[주사위 굴림]-> [성공/실패 결정]-> [결과 묘사(그림, 텍스트)]
{1}로 이동, 반복...

---------
캐릭터 클래스

아이템 클래스
"""

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




