import requests
import time
import os

API_KEY = os.getenv("SUNO_API_KEY")

BASE_URL = "https://api.sunoapi.org/api/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def generate_song(prompt):
    try:
        # 1. создаём задачу
        response = requests.post(
            f"{BASE_URL}/generate",
            json={
                "prompt": prompt,
                "customMode": False,
                "instrumental": False,
                "model": "V3_5"
            },
            headers=headers
        )

        data = response.json()
        print("Generate response:", data)

        if data.get("code") != 200:
            return f"❌ Ошибка API: {data}"

        task_id = data["data"]["taskId"]

        # 2. ждём результат
        for _ in range(20):
            res = requests.get(
                f"{BASE_URL}/get?taskId={task_id}",
                headers=headers
            ).json()

            print("Status:", res)

            if res.get("code") == 200:
                songs = res["data"].get("songs", [])
                if songs:
                    return songs[0]["audio_url"]

            time.sleep(3)

        return "❌ Не удалось получить трек (таймаут)"

    except Exception as e:
        print("Ошибка:", e)
        return "❌ Ошибка генерации"
