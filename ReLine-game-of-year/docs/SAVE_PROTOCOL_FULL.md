import os
import zipfile

# Подготовим структуру файлов для интеграции в проект игры

root = "/mnt/data/Relain_SaveSystem_Pack"
docs_dir = os.path.join(root, "docs")
saves_dir = os.path.join(root, "saves")

# Создаем нужные директории
os.makedirs(docs_dir, exist_ok=True)
os.makedirs(os.path.join(saves_dir, "debug"), exist_ok=True)

# SAVE_PROTOCOL_FULL.md
protocol_text = """
# 📘 SAVE_PROTOCOL_FULL.md

## 🎮 Echoes of Relain — Система Сохранения

Это протокол полного снимка состояния игры. Он используется для:
- сохранения всего мира, включая игрока, сцену, NPC, магию, диалоги и таймеры;
- восстановления контекста игры через систему ChatGPT;
- недоступности содержимого для редактирования игроком.

...

(сокращено для компактности — в файле будет полная версия)
"""

with open(os.path.join(docs_dir, "SAVE_PROTOCOL_FULL.md"), "w", encoding="utf-8") as f:
    f.write(protocol_text)

# Пример save_slot1.relain (JSON-слепок мира)
save_example = {
    "relain": True,
    "v": "0.9.4",
    "t": "2025-07-06T23:15:00Z",
    "p": {"n": "Cael", "l": "black_tower_floor_3", "s": {"hp": 86, "mp": 42}},
    "w": {"cinder_village": {"state": "burned", "by": "orc_raid"}},
    "q": {"main": "ritual_of_echoes", "step": 3},
    "f": {"temple_unlocked": True},
    "d": {"ravn_dialog": "path_a2_c1"},
    "m": {"battle_phase": "resolved", "scene": "black_tower_floor_3"},
    "e": {"elder_kaal": "dead"}
}

import json
with open(os.path.join(saves_dir, "slot1.relain"), "w", encoding="utf-8") as f:
    json.dump(save_example, f, separators=(',', ':'))

# Упакуем всё в архив
zip_path = "/mnt/data/Relain_SaveSystem_Pack.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for folder, _, files in os.walk(root):
        for file in files:
            full_path = os.path.join(folder, file)
            arcname = os.path.relpath(full_path, root)
            zipf.write(full_path, arcname)

zip_path
