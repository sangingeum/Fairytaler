import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
from ResourcePool import *

class StoryManager:
    def __init__(self):
        self.story = ""
        self.resource_pool = []
    # basic operations
    def save(self):
        pass
    def load(self):
        pass
    def start(self):
        pass
    def end(self):
        pass
    def init(self):
        pass
    # storty operations
    def tell_story(self):
        pass
    def tell_event(self):
        pass
    def generate_event(self):
        pass
    def create_choices(self):
        pass
    def summarize(self):
        pass
    def is_dead(self):
        pass




