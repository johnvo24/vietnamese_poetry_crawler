from google import genai
from google.genai import types
import os

class GeminiAI():
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        
    def generate(self, prompt):
        response =  self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"Yêu cầu: Bây giờ tôi đưa bài thơ hoàn chỉnh. Hãy làm cho nó có lỗi sao cho vẫn tự nhiên giống con người nhất. Các lỗi gồm: Vần, Âm luật, Ngữ pháp, Ngữ nghĩa, Dấu câu.\nHãy tạo thơ lỗi theo yêu cầu (giữ nguyên số lượng từ mỗi câu) và chỉ trả về phản hồi nội dung thơ lỗi (thơ lỗi phải khác thơ hoàn chỉnh): {prompt}",
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1000
            ),
        )
        return response

# for i in range(0, 1):
#     print(generate(prompt="Viết bài thơ lục bát tặng mẹ ngày 8/3").text)
#     time.sleep(random.uniform(1, 2))
    
# geminiAI = GeminiAI()
# print(geminiAI.generate("Thương nhớ ơ hờ, thương nhớ ai?\nSông xa từng lớp lớp mưa dài\nMắt kia em có sầu cô quạnh\nKhi chớm heo về một sớm mai?\nRét mướt mùa sau chừng sắp ngự\nBên này em có nhớ bên kia\nGiăng giăng mưa bụi quanh phòng tuyến\nHiu hắt chiều sông lạnh bến Tề\nKhói thuốc xanh dòng khơi lối xưa\nĐêm đêm sông Đáy lạnh đôi bờ\nThoáng hiện em về trong đáy cốc\nNói cười như chuyện một đêm mơ\nXa quá rồi em người mỗi ngã\nBên này đất nước nhớ thương nhau\nEm đi áo mỏng buông hờn tủi\nDòng lệ thơ ngây có dạt dào ?").text)
# print(geminiAI.generate("Bình phương kết quả trên").text)