from flask import Flask, request
import vk_api
from vk_api.utils import get_random_id
from suno import generate_song

app = Flask(__name__)

# 🔑 ВСТАВЬ СЮДА
VK_TOKEN = "ТВОЙ_VK_ТОКЕН"
CONFIRMATION_TOKEN = "b34ed879"

vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()

users = {}

questions = [
    "Какой стиль музыки? (рэп, поп, рок)",
    "О чём песня?",
    "Для кого песня?",
    "Какое настроение?",
    "Добавить конкретные слова или имя?"
]

def send_message(user_id, text):
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=get_random_id()
    )

@app.route('/', methods=['POST'])
def callback():
    data = request.json

    if data['type'] == 'confirmation':
        return CONFIRMATION_TOKEN

    if data['type'] == 'message_new':
        user_id = data['object']['message']['from_id']
        text = data['object']['message']['text']

        if user_id not in users:
            users[user_id] = {"step": 0, "answers": []}
            send_message(user_id, "Привет! 🎵 Создадим тебе песню")
            send_message(user_id, questions[0])
            return "ok"

        user = users[user_id]

        user["answers"].append(text)
        user["step"] += 1

        if user["step"] < len(questions):
            send_message(user_id, questions[user["step"]])
        else:
            send_message(user_id, "⏳ Генерирую песню...")

            prompt = f"""
Create a song:

Genre: {user['answers'][0]}
Theme: {user['answers'][1]}
For: {user['answers'][2]}
Mood: {user['answers'][3]}
Details: {user['answers'][4] if len(user['answers']) > 4 else ""}

Make it catchy and emotional.
"""

            audio_url = generate_song(prompt)

            send_message(user_id, "🎧 Готово!")
            send_message(user_id, audio_url)

            del users[user_id]

    return "ok"

if __name__ == "__main__":
    app.run(port=10000)
