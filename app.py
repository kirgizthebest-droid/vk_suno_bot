from flask import Flask, request
import requests
import os
import threading
from suno import generate_song

app = Flask(__name__)

VK_TOKEN = os.getenv("VK_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

users = {}


def send_message(user_id, text):
    requests.get(
        "https://api.vk.com/method/messages.send",
        params={
            "user_id": user_id,
            "message": text,
            "random_id": 0,
            "access_token": VK_TOKEN,
            "v": "5.131"
        }
    )


def process_song(user_id, prompt):
    audio_url = generate_song(prompt)

    if "http" in audio_url:
        send_message(user_id, f"🎧 Готово:\n{audio_url}")
    else:
        send_message(user_id, audio_url)


@app.route("/", methods=["POST"])
def callback():
    data = request.json

    if data["type"] == "confirmation":
        return os.getenv("CONFIRMATION_TOKEN")

    if data["type"] == "message_new":
        user_id = data["object"]["message"]["from_id"]
        text = data["object"]["message"]["text"]

        # запускаем генерацию в фоне
        threading.Thread(
            target=process_song,
            args=(user_id, text)
        ).start()

        send_message(user_id, "🎵 Генерирую песню...")

    return "ok"


if __name__ == "__main__":
    app.run()
