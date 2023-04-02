from openai_utils import *
from ResourcePool import *
import random
import re

# TODOS:
# equipment, item system 구현
# companion 고려한 야야기, 이벤트 생성
# 처음 보는 사이인데 마치 아는 사이인 것처럼 행동하는 경우가 있다. 고치자.
# 종족 고려하여 인물 성별 자동 설정하는 기능(기본, 종족별..)
# companion describe function
# openai 부분 따로 분리
# complete the event 방식으로 가야하지 않을까

# 선택지 고민: 행동이나 대사를 직접 선택하게 하지 말고 행동이나 대사의 주제를 정해주면 속 내용은 알아서 채워지게..
# 예를 들어, [도망] [공격] [대화] 이러한 선택지가 나오고 플레이어는 이 중에서 선택하면 되는 방식으로



class StoryManager:
    def __init__(self):
        self.writer_prompt = "You are a story writer who writes an interesting fantasy story." \
                            "\nYour story can be a bit violent for the sake of realism." \
                            "\nYour job is to write an engaging story full of adventures and events."

        self.assistant_prompt = "You are a helpful assistant."

        self.story = "\nStory:" \
                     "\nRobin finally reached a forest."

        self.event = "\nEvent:" \
                     "\n{}"

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
        self.protagonist = self.resource_pool.characters[0]
        self.event_prob = 1



    # basic operations
    def save(self, path):
        pass
    def load(self, path):
        pass

    def start(self):
        self.tell_story()


    def end(self):
        pass
    def init(self):
        pass
    # story operations

    def tell_story(self):

        if random.uniform(0, 1) < self.event_prob:
            print("event")
            # event
            if len(self.resource_pool.characters) < 2:
                self.resource_pool.create_character()
            sampled_character = random.sample(self.resource_pool.characters[1:], k=1)[0]

            print(self.protagonist.to_dict())
            print(sampled_character.to_dict())

            system_prompt = self.writer_prompt

            characters_info = self.characters_info_format.format(
                [self.protagonist.to_dict(), sampled_character.to_dict()])
            user_prompt = self.story + characters_info + self.protagonist.describe_relationship(sampled_character)\
                          + self.story_request_prompt + self.character_constraints
            next_story = get_answer(system_prompt, user_prompt)

            print(next_story)

            self.tell_event(next_story, self.protagonist, sampled_character)

        else:
            print("non event")
            print(self.protagonist.to_dict())

            system_prompt = self.writer_prompt
            user_prompt = self.story + self.character_constraints + self.story_request_prompt
            next_story = get_answer(system_prompt, user_prompt)
            print(next_story)


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



