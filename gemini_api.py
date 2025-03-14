from google import genai
from google.genai import types
import os

class GeminiAI():
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        
    def generate(self, prompt):
        response =  self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=200
            ),
        )
        return response

# for i in range(0, 1):
#     print(generate(prompt="Viết bài thơ lục bát tặng mẹ ngày 8/3").text)
#     time.sleep(random.uniform(1, 2))
    
geminiAI = GeminiAI()
print(geminiAI.generate("1 + 1 bằng bao nhiêu?").text)
print(geminiAI.generate("Bình phương kết quả trên").text)