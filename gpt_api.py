# import openai

# class ChatGPTClient:
#     def __init__(self, api_key, model="gpt-4o-mini"):
#         self.api_key = api_key
#         self.model = model
    
#     def chat(self, message, stream=False):
#         client = openai.OpenAI(api_key=self.api_key)
#         response = client

from openai import OpenAI

client = OpenAI()

chat_completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
)

print(chat_completion.choices[0].message)