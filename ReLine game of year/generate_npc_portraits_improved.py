
import os
import json
import base64
import requests
from PIL import Image
from io import BytesIO

api_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
json_file = "npc_portraits_prompts_improved.json"
output_dir = "npc_portraits"
os.makedirs(output_dir, exist_ok=True)

with open(json_file, "r", encoding="utf-8") as f:
    prompts = json.load(f)

print(f"🔍 Загружено {len(prompts)} промтов")

for entry in prompts:
    file_name = entry["file_name"] + ".png"
    prompt_text = entry["prompt"]
    output_path = os.path.join(output_dir, file_name)

    payload = {
        "prompt": prompt_text,
        "negative_prompt": "lowres, blurry, jpeg artifacts, poorly drawn face, malformed proportions, extra eyes",
        "steps": 30,
        "cfg_scale": 8.0,
        "width": 512,
        "height": 512,
        "sampler_name": "DPM++ 2M Karras"
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        result = response.json()
        image_data = result["images"][0]
        image_bytes = base64.b64decode(image_data.split(",", 1)[-1])
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        image_resized = image.resize((128, 128), Image.NEAREST)
        image_resized.save(output_path)
        print(f"✅ Сохранён портрет: {file_name}")

    except Exception as e:
        print(f"❌ Ошибка при генерации {file_name}: {e}")
