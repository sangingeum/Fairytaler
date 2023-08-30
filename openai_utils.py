import openai
import json
import os
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_answer(user_prompt, system_prompt=None, return_token=False):
    messages = []
    if system_prompt is not None:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",# ["gpt-4", "gpt-3.5-turbo"]
        messages=messages
    )
    answer = response["choices"][0]["message"]["content"]
    if return_token:
        token_used = response['usage']['total_tokens']
        return answer, token_used
    return answer



