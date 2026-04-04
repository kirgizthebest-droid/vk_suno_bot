from flask import Flask, request
import vk_api
from vk_api.utils import get_random_id
from suno import generate_song

app = Flask(__name__)

# 🔑 ВСТАВЬ СЮДА
VK_TOKEN = "vk1.a.yHRjlGZz32DpRfH6EP9s3_pFOC12x8Rr_JvuAIpKW2Y4P8A5G1bJKr5qYLr_4CAxC7-gDTKFcoKaXtWLf9iPek82vvVB8AbxJkSBbvCwIzNfnxQBJk8acUjmzLdp79SFGsfY0g3CHAYVTtA3VRruyU9WrnA-3evntzrjUBeD2l06EQ1YRk2FrhwCtKfJPCGPiBaGu_kkhInzT7NWRF-Zig"
CONFIRMATION_TOKEN = "31a3887e"

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

            import threading
from suno import generate_song


def process_song(user_id, prompt):
    audio_url = generate_song(prompt)

    if "http" in audio_url:
        send_message(user_id, f"🎧 Готово:\n{audio_url}")
    else:
        send_message(user_id, audio_url)


# внутри callback:
threading.Thread(
    target=process_song,
    args=(user_id, prompt)
).start()

send_message(user_id, "🎵 Генерирую песню...")
return "ok"
        del users[user_id]
    return "ok"

if __name__ == "__main__":
    app.run(port=10000)
