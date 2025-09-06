import discord, re, os
from dotenv import load_dotenv
from discord.errors import HTTPException
import gemini_api_call
load_dotenv()

client = discord.Client(intents=discord.Intents.default())

# 起動時に動作する処理
@client.event
async def on_ready():

    # 起動したらターミナルにログイン通知が表示される
    print('起動完了。救済可能。')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # メッセージ生成処理
    if message.content != '':
        await reply_message(message)

# メッセージ送信処理
async def reply_message(message):

    # 宛先の削除
    message.content = re.sub(r'<[^>]*>', '', message.content)

    # AIで翻訳
    translation = gemini_api_call.generate(message.content)

    # 生成された回答を送信
    try:
        await message.channel.send(translation)

    except HTTPException as e:
        print(e)
        # AIからの回答が無い場合の文章送信処理
        await message.channel.send(f"翻訳に失敗しました。번역에 실패했습니다.")

client.run(token=os.getenv("BOT_ACCESS_TOKEN"))