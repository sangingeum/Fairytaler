import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_answer(system_prompt, user_prompt, return_token=False):
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