import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

# 検閲レベル設定
SAFTY_SETTINGS = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
]

def generate(input):

    # 翻訳用プロンプト変換
    prompt = create_prompt(input)
    print(prompt)

    # AIクライアント定義
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # 文章生成
    answer = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(safety_settings=SAFTY_SETTINGS)
    )

    return answer.text

def create_prompt(input):
    prompt = f"""
You are a translation app used by Japanese and Korean speakers.
- If the input is in Japanese, translate it into Korean.
- If the input is in Korean, translate it into Japanese.
- Only output the translation result. Do not add explanations or comments.

input: {input}
"""
    return prompt