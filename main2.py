from openai import OpenAI
from hidden_vars import *

#OpenAI.api_key = OPENAI_API_KEY

client = OpenAI(
    api_key = OPENAI_API_KEY
)


def chatGPT(prompt):
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo', #GPT Version
        messages = [{'role': 'user', "content": prompt}]
    )

    return response.choices[0].message()

if __name__ == "__main__":
    while True:
        userInput = input("You: ")
        if userInput.lower() in ['quit', 'exit', 'bye']:
            break
        response = chatGPT(userInput)
        print("Chatbot: ", response)

''' Sample API usage in Python from https://platform.openai.com/docs/models?lang=python

from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)

'''