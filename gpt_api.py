from openai import OpenAI
import time

client = OpenAI()

chat_completion = client.chat.completions.create(
    model="gpt-4o",
    store=True,
    messages=[
        {
            "role": "user",
            "content": "Create a poem about Vietnamese.",
        }
    ],
)
while True:
    print(chat_completion.choices[0].message)
    time.sleep(1)