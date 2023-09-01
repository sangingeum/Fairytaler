from openai_utils import *
from ResourcePool import *
from ImageCreator import *
import random
import re

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
        self.writer_prompt = "You are a story writer who writes an interesting fantasy story." \
                            "\nYour story can be a bit violent for the sake of realism." \
                            "\nYour job is to write an engaging story full of adventures and events."

        self.assistant_prompt = "You are a helpful assistant."

        self.story = ""

        self.event_commands_continue = "\nCommands:" \
                                       "\nDescribe what characters do or say after the event." \
                                       "\nYou can also describe the consequences of the actions taken in the event." \
                                       "\nDo not include {}'s action, thought, or line" \
                                       "\nLimit the number of sentences you use to between 1 and 2."

        self.event_commands_terminate = "\nCommands:" \
                                        "\nYou describe what characters do or say after this event." \
                                        "\nYou also describe what happens as a result of actions taken in this event." \
                                        "\nEnd the story using {} sentences at most."

        self.character_commands_choices = "\nCommands:" \
                                          "\nList {} actions that {} possibly do after the event." \
                                          "\nEach action should be expressed within {} words." \
                                          "\nExamples of actions are 'Attack [target's name]', 'Talk to [target's name] about [topic]', and 'Steal [item name] from [target's name]'." \
                                          "\nEach action should start with a number specifying its order." \
                                          "\nEach action should be distinct."

        self.character_commands_execution = "\nCommands:" \
                                            "\nDescribe what {} possibly does or says if he/she wants to '{}' after the event" \
                                            "\nFollow the writing style of the event." \
                                            "\nLimit the number of sentences you use to between 1 and 3."

        self.writer_commands_continue = "\nWrite the next possible story in a sentence."\
                                         "\nThe story can be incomplete." \
                                         "\nThe story should cover only a single event." \
                                         "\nDo not add any character in the story." \
                                         "\nDo not add any place in the story."

        self.character_constraints = "\nConstraints:" \
                                     "\nCharacters in this story don't know each other's name, personality, background or items unless they are told or see." \
                                     "\nIt is common that characters don't easily trust each other." \
                                     "\nCharacters do not cooperate until they know each other." \
                                     "\nIf a character's compainons variable is empty, it means the character is currently alone."

        self.characters_info_format = "\nInformation about characters:" \
                                      "\n{}"

        self.story_request_prompt = "\nWrite the next possible story in a sentences." \
                                    "\nThe story can be incomplete." \
                                    "\nThe story should cover only a single event." \
                                    "\nDo not add any character in the story." \
                                    "\nDo not add any place in the story."

        self.resource_pool = ResourcePool()
        self.resource_pool.load_resource()
        self.image_creator = ImageCreator()
        self.protagonist = None
        self.universe = None


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
        prompt = """I want you to act as a novel writer.
The fictional universe of the story is like this : {}
Introduce the fictional universe while not mentioning any named characters.
""".format(self.universe)
        self.universe = get_answer(prompt)
        # print the universe description
        print(self.universe)
        # Create initial image
        image_prompt = create_prompt(prompt)
        self.image_creator.create(image_prompt["prompt"], image_prompt["negative_prompt"])

    def tell_story(self):
        command = """I want you to act as the GM of a TRPG game based on the universe and characters written below.
When a character attempts critical actions such as attacks, escapes, and evades, you need to determine the success or failure of the attempt by rolling a 1d20 die.
A roll of 10 or above indicates success, while anything below 10 is a failure.
Equipments, companions, relationships, and status of {0} can change during the playthrough.
It's your responsibility to update them correctly. When it is {0}'s turn, stop writing and wait for his/her answer.
I'll play as {0}.
""".format(self.protagonist.name)

        info = """
Fictional universe:
{}

Protagonist information:
{}
""".format(self.universe, self.protagonist.describe())
        user_prompt = command + info
        messages=[]
        while True:
            messages.append({"role": "user", "content": user_prompt})
            assistant_answer = chat_completion(messages)
            messages.append({"role": "assistant", "content": assistant_answer})
            #print(user_prompt)
            print(assistant_answer)
            # Create image
            image_prompt = create_prompt(assistant_answer)
            self.image_creator.create(image_prompt["prompt"], image_prompt["negative_prompt"])

            user_prompt = input(":")



    def tell_event(self, next_story, character_from, character_to):
        choice_num = 5
        event_turn = random.randint(3, 5)
        cur_event = next_story

        while True:
            supporting_character_lines = self.create_supporting_character_lines(cur_event, character_from, character_to, event_turn)
            cur_event += "\n" + supporting_character_lines

            event_turn -= 1
            if event_turn == 0:
                break

            choices = self.create_choice(choice_num, cur_event, character_from, character_to)
            selected_choice = self.select_choice(choices, choice_num)
            print()
            print(selected_choice)

            action = self.execute_choice(selected_choice, cur_event, character_from, character_to)
            print()
            print(action)

            cur_event += "\n" + action


        #relationship, companion, background update | event summaray
        updated_relationship = self.update_relationship(cur_event, character_from, character_to)
        print("updated_relationship")
        print(updated_relationship)
        updated_companion_status = self.update_companion(cur_event, character_from, character_to)
        print("updated_companion_status")
        print(updated_companion_status)
        updated_background1 = self.update_background(cur_event, character_from)
        updated_background2 = self.update_background(cur_event, character_to)
        print("updated_background1")
        print(updated_background1)
        print("updated_background2")
        print(updated_background2)
        story_summary = self.update_story(cur_event)
        print("story_summary")
        print(story_summary)


    def create_supporting_character_lines(self, event, character_from, character_to, event_turn):

        if event_turn <= 1:
            event_commands = self.event_commands_terminate.format(4)
        else:
            event_commands = self.event_commands_continue.format(character_from.name)

        system_prompt = self.writer_prompt

        characters_info = self.characters_info_format.format([character_from.to_dict(), character_to.to_dict()])
        user_prompt = self.story + self.event.format(event) + characters_info + character_from.describe_relationship(character_to) + self.character_constraints + event_commands

        supporting_character_lines = get_answer(system_prompt, user_prompt)

        print("/prompts")
        print(system_prompt)
        print(user_prompt)
        print("prompts/")
        print()
        print(supporting_character_lines)

        return supporting_character_lines


    def execute_choice(self, selected_choice, event, character_from, character_to):
        system_prompt = self.writer_prompt
        characters_info = self.characters_info_format.format([character_from.to_dict(), character_to.to_dict()])
        user_prompt = self.story + self.event.format(event) + characters_info \
                      + character_from.describe_relationship(character_to) + self.character_constraints \
                      + self.character_commands_execution.format(character_from.name, selected_choice)
        action = get_answer(system_prompt, user_prompt)
        print("/prompts")
        print(system_prompt)
        print(user_prompt)
        print("prompts/")

        print(action)

        return action

    def create_choice(self, choice_num, event, character_from, character_to):
        system_prompt = self.assistant_prompt
        characters_info = self.characters_info_format.format([character_from.to_dict(), character_to.to_dict()])
        user_prompt = self.story + self.event.format(event) + characters_info \
                      + character_from.describe_relationship(character_to) + self.character_constraints \
                      + self.character_commands_choices.format(choice_num, character_from.name, 6)
        unparsed_choices = get_answer(system_prompt, user_prompt)
        print("/prompts")
        print(system_prompt)
        print(user_prompt)
        print("prompts/")
        unparsed_choices = re.findall(r'[0-9]+\.\s(.*?)\n', unparsed_choices + "\n\n")
        print(unparsed_choices)
        print()
        print(unparsed_choices)
        return unparsed_choices


    def update_relationship(self, event, character_A, character_B):
        system_prompt = self.assistant_prompt
        event_prompt = "Event:" \
                       "\n{}".format(event)
        user_prompt = event_prompt + character_A.describe_relationship(character_B) + "\nWrite down the updated opinion of {} on {} and vise versa." \
                                                                                      "\nFollow this format:" \
                                                                                      "\n{}: [{}'s opinion on {}]" \
                                                                                      "\n{}: [{}'s opinion on {}]" \
                                                                                      "\nLimit the number of sentences you use for each opinion to {}".format(character_A.name, character_B.name,
                                                                                                                                                              character_A.name, character_A.name, character_B.name,
                                                                                                                                                              character_B.name, character_B.name, character_A.name,
                                                                                                                                                              3)
        updated_relationship = get_answer(system_prompt, user_prompt)
        character_A.relationships[character_B.name] = updated_relationship
        character_B.relationships[character_A.name] = updated_relationship
        return updated_relationship


    def update_companion(self, event, character_A, character_B):
        system_prompt = self.assistant_prompt
        event_prompt = "Story:" \
                       "\n{}".format(event)
        user_prompt = event_prompt + "\nIs {} with {} currently? Answer in 'YES' or 'NO'" \
                                     "\nIf there is no explicit separation between them, answer with YES.".format(character_A.name, character_B.name)

        updated_companion_status = get_answer(system_prompt, user_prompt).lower()

        if updated_companion_status == "no":
            updated_companion_status = "Not Together"
        else:
            updated_companion_status = "Together"

        character_A.companions[character_B.name] = updated_companion_status
        character_B.companions[character_A.name] = updated_companion_status

        return updated_companion_status

    def update_background(self, event, character):
        system_prompt = self.assistant_prompt
        event_background_format = "Event:" \
                                   "\n{}" \
                                   "\n{}'s background:" \
                                   "\n{}".format(event, character.name, character.background)
        user_prompt = event_background_format + "\nUpdate {}'s background considering the event." \
                                                "\nLimit the number of sentences you use to between 1 and {}".format(character.name, 3)
        changed_background = get_answer(system_prompt, user_prompt)
        character.background = changed_background
        return changed_background

    def update_story(self, event):
        system_prompt = self.assistant_prompt
        user_prompt = "\n{}"\
                      "\nSummarize the story within {} sentences."\
                      "\nYou can omit unimportant details to shoten the story." \
                      "\nIf think you don't need to edit the story, leave it as it is.".format(self.story + event, 20)

        summary = get_answer(system_prompt, user_prompt)
        self.story = "\nThe story so far was like this:" \
                     "\n" + summary
        return summary


    def select_choice(self, choices, choice_num):
        n = self.select_number(choice_num)
        if n == -1:
            print("Enter your own choice")
            selected_choice = str(input())
        else:
            selected_choice = choices[n]
        return selected_choice
    def select_number(self, choice_num):
        print("Enter a number between 0 and {}. Enter -1 to make your own choice.".format(choice_num - 1))
        n = int(input())
        while n < -1 and n >= choice_num:
            print("(RE) Enter a number between 0 and {}".format(choice_num - 1))
            n = int(input())
        return n
    def is_dead(self):
        pass



