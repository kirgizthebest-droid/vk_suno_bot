import requests
import os
import time

# 👉 ВСТАВЬ API В Render (НЕ СЮДА)
SUNO_API_KEY = os.getenv("1b9544b2a524d363c7ad40babfcf058e")

# ⚠️ ЗАМЕНИ если у тебя другой endpoint
BASE_URL = "https://api.suno.ai/v1/generate"

def generate_song(prompt):
    headers = {
        "Authorization": f"Bearer {SUNO_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": prompt
    }

    try:
        # 1. отправляем генерацию
        response = requests.post(BASE_URL, json=data, headers=headers)
        result = response.json()

        print("Suno response:", result)

        # если сразу вернуло аудио
        if "audio_url" in result:
            return result["audio_url"]

        task_id = result.get("id")

        # 2. проверяем статус
        status_url = f"https://api.suno.ai/v1/status/{task_id}"

        for _ in range(20):
            status_res = requests.get(status_url, headers=headers).json()
            print("Status:", status_res)

            if status_res.get("status") == "completed":
                return status_res.get("audio_url")

            time.sleep(3)

        return "❌ Не удалось сгенерировать песню"

    except Exception as e:
        print("Ошибка Suno:", e)
        return "❌ Ошибка при генерации"
