import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
from ResourcePool import *
import random
import re

# to do:
# equipment, item system 구현
# companion 고려한 야야기, 이벤트 생성
# 처음 보는 사이인데 마치 아는 사이인 것처럼 행동하는 경우가 있다. 고치자.
# 종족 고려하여 인물 성별 자동 설정하는 기능(기본, 종족별..)
#
# 선택지 고민: 행동이나 대사를 직접 선택하게 하지 말고 행동이나 대사의 주제를 정해주면 속 내용은 알아서 채워지게..
# 예를 들어, [도망] [공격] [대화] 이러한 선택지가 나오고 플레이어는 이 중에서 선택하면 되는 방식으로


class StoryManager:
    def __init__(self):
        self.story_teller = "You are a story writer who writes an interesting fantasy story." \
                            "\nYour story can be a bit cruel for the sake of realism." \
                            "\nYour job is to write an engaging story full of adventures and events."

        self.event_teller = "\nEvent: {}" \
                            "\nYou describe what characters do or say after this event." \
                            "\nYou also describe what happens as a result of actions taken in this event." \
                            "\nDo not include {}'s action, thought, or line" \
                            "\nThe description can be incomplete." \
                            "\nLimit the number of sentences you use to between 1 and 2."

        self.event_terminator = "\nEvent: {}" \
                                "\nYou describe what characters do or say after this event." \
                                "\nYou also describe what happens as a result of actions taken in this event." \
                                "\nEnd the story using {} sentences at most."

        self.character_teller = "\nEvent: {}" \
                                "\nDescribe what {} possibly does or says after the event." \
                                "\nDo not describe consequences of {}'s action." \
                                "\nDo not describe actions or reactions from other characters." \
                                "\nList {} different descriptions." \
                                "\nEach description should be distinct." \
                                "\nEach description should start with a number specifying its order."

        self.story = "\nThe story so far was like this:" \
                     "\nRobin finally reached a forest."

        self.story_request_prompt = "\nWrite the next possible story in a sentence."\
                                     "\nThe story can be incomplete." \
                                     "\nThe story should cover only a single event." \
                                     "\nDo not add any character in the story." \
                                     "\nDo not add any place in the story."

        self.character_constraints = "\nCharacter constraints:" \
                                     "\nCharacters in this story don't know each other's name, personality, background or items unless they are told or see." \
                                     "\nIt is common that characters don't easily trust each other." \
                                     "\nCharacters do not cooperate until they know each other." \
                                     "\nIf a character's compainons variable is empty, it means the character is currently alone."
        self.characters_info_format = "\nInformation about characters:" \
                                      "\n{}"

        self.event_request_with_conditions_choices = "\nWrite {} possible lines you would say to {}." \
                                                     "\nWrite {} possible actions you would take in this situation."

        self.event_request_with_conditions_single_choice = "\n{} possible lines you would say to {}." \

        self.event_request_with_conditions = ""
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

    def get_answer(self, system_prompt, user_prompt, return_token=False):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",
                 "content": user_prompt}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        if return_token:
            token_used = response['usage']['total_tokens']
            return answer, token_used
        return answer

    def tell_story(self):

        if random.uniform(0, 1) < self.event_prob:
            print("event")
            # event
            if len(self.resource_pool.characters) < 2:
                self.resource_pool.create_character()
            sampled_characters = random.sample(self.resource_pool.characters, 2)
            sampled_character = sampled_characters[0] if sampled_characters[0] != self.protagonist else sampled_characters[1]
            print(self.protagonist.to_dict())
            print(sampled_character.to_dict())

            characters_info = self.characters_info_format.format([self.protagonist.to_dict(), sampled_character.to_dict()])
            system_prompt = self.story_teller
            user_prompt = self.story + self.character_constraints + characters_info + self.story_request_prompt
            next_story = self.get_answer(system_prompt, user_prompt)

            print(next_story)

            self.tell_event(next_story, self.protagonist, sampled_character)

        else:
            print("non event")
            print(self.protagonist.to_dict())

            system_prompt = self.story_teller
            user_prompt = self.story + self.character_constraints + self.story_request_prompt
            next_story = self.get_answer(system_prompt, user_prompt)
            print(next_story)


    def tell_event(self, next_story, character_from, character_to):
        choice_num = 3
        event_turn = random.randint(3, 5)
        cur_event = next_story

        while True:
            supporting_character_lines = self.create_supporting_character_lines(cur_event, character_from, character_to, event_turn)
            cur_event += "\n" + supporting_character_lines

            event_turn -= 1
            if event_turn == 0:
                break
            choices = self.create_protagonist_choices(choice_num, cur_event, character_from, character_to)

            print("Enter a number between 0 and {}".format(choice_num - 1))
            n = int(input())
            while n < 0 and n >= choice_num:
                print("(RE) Enter a number between 0 and {}".format(choice_num - 1))
                n = int(input())
            choice = choices[n]
            print()
            print(choice)
            cur_event += "\n" + choice


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
            event_teller = self.event_terminator.format(event, 4)
        else:
            event_teller = self.event_teller.format(event, character_from.name)

        characters_info = self.characters_info_format.format([character_from.to_dict(), character_to.to_dict(), character_from.describe_relationship(character_to)])
        system_prompt = self.story_teller
        user_prompt = self.story + self.character_constraints + characters_info + event_teller

        supporting_character_lines = self.get_answer(system_prompt, user_prompt)

        print("/prompts")
        print(system_prompt)
        print(user_prompt)
        print("prompts/")
        print()
        print(supporting_character_lines)

        return supporting_character_lines


    def create_protagonist_choices(self, choice_num, event, character_from, character_to):
        #event_teller = self.event_teller.format(next_story, character_from.name)
        character_teller = self.character_teller.format(event, character_from.name, character_from.name, character_from.name, choice_num)
        characters_info = self.characters_info_format.format([character_from.to_dict(), character_to.to_dict(), character_from.describe_relationship(character_to)])
        system_prompt = self.story_teller
        user_prompt = self.story + self.character_constraints + characters_info + character_teller
        unparsed_protagonist_choices = self.get_answer(system_prompt, user_prompt)
        print("/prompts")
        print(system_prompt)
        print(user_prompt)
        print("prompts/")
        protagonist_choices = re.findall(r'[0-9]+\.\s(.*?)\n', unparsed_protagonist_choices + "\n\n")
        print(unparsed_protagonist_choices)
        print()
        print(protagonist_choices)
        return protagonist_choices

    def update_relationship(self, event, character_A, character_B):
        system_prompt = "You are a helpful assistant."
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
        updated_relationship = self.get_answer(system_prompt, user_prompt)
        character_A.relationships[character_B.name] = updated_relationship
        character_B.relationships[character_A.name] = updated_relationship
        return updated_relationship


    def update_companion(self, event, character_A, character_B):
        system_prompt = "You are a helpful assistant."
        event_prompt = "Story:" \
                       "\n{}".format(event)
        user_prompt = event_prompt + "\nIs {} with {} currently? Answer in 'YES' or 'NO'".format(character_A.name, character_B.name)
        updated_companion_status = self.get_answer(system_prompt, user_prompt)
        character_A.companions[character_B.name] = updated_companion_status
        character_B.companions[character_A.name] = updated_companion_status
        return updated_companion_status

    def update_background(self, event, character):
        system_prompt = "You are a helpful assistant."
        event_background_format = "Event:" \
                                   "\n{}" \
                                   "\n{}'s background:" \
                                   "\n{}".format(event, character.name, character.background)
        user_prompt = event_background_format + "\nUpdate {}'s background considering the event." \
                                                "\nLimit the number of sentences you use to {}".format(character.name, 3)
        changed_background = self.get_answer(system_prompt, user_prompt)
        character.background = changed_background
        return changed_background

    def update_story(self, event):
        system_prompt = "You are a helpful assistant."
        user_prompt = "\n{}"\
                      "\nSummarize the story in {} sentences"\
                      "\nYou can omit unimportant details to shoten the story.".format(self.story + event, 20)

        summary = self.get_answer(system_prompt, user_prompt)
        self.story = "\nThe story so far was like this:" \
                     "\n" + summary
        return summary
    def is_dead(self):
        pass



