import os
import shutil
import logging
import re

SOURCE_DIR = "ReLine-game-of-year"
LOG_FILE = "migration_log.txt"

MAPPING = {
    "generate_npc_portraits_improved.py": "core/",
    "relain_dason.json": "core/",
    "assets_manifest.json": "data/",
    "dason.json": "data/",
    "relayindesign.json": "data/",
    "relain_game_expanded.json": "data/",
    "lore_index.json": "data/",
    "npc_portrait_index.json": "data/",
    "structure.txt": "data/",
    "pixel_prompts_named.json": "prompts/",
    "npc_portraits_prompts_improved.json": "prompts/",
    "icons/icons_prompts.json": "prompts/",
    "transport/transport_pack.zip": "transport/",
    "bettiary/": "lore/bettiary/",
    "magic/": "lore/magic/",
    "system/": "lore/system/",
    "online/": "lore/online/",
    "panteon/": "lore/panteon/",
    "world/": "lore/world/",
    "characters/": "assets/characters/",
    "effects/": "assets/effects/",
    "environment/": "assets/environment/",
    "icons/": "assets/icons/",
    "items/": "assets/items/",
    "map/": "assets/map/",
    "monster/": "assets/monster/",
    "npc_portraits/": "assets/npc_portraits/",
    "player_portraits/": "assets/player_portraits/",
    "scenes/": "assets/scenes/",
    "spells/": "assets/spells/",
    "ui/": "assets/ui/"
}

PATH_REPLACEMENTS = {
    "icons/": "assets/icons/",
    "npc_portraits/": "assets/npc_portraits/",
    "characters/": "assets/characters/",
    "items/": "assets/items/",
    "map/": "assets/map/",
    "monster/": "assets/monster/",
    "scenes/": "assets/scenes/",
    "spells/": "assets/spells/",
    "effects/": "assets/effects/",
    "ui/": "assets/ui/",
    "magic/": "lore/magic/",
    "panteon/": "lore/panteon/",
    "world/": "lore/world/",
    "system/": "lore/system/",
    "bettiary/": "lore/bettiary/"
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def move_item(src, dest):
    ensure_dir(os.path.dirname(dest))
    if os.path.isdir(src):
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.move(src, dest)
    else:
        shutil.move(src, dest)

def remove_empty_dirs(root):
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)
            logging.info(f"Removed empty directory: {dirpath}")

def update_paths_in_text(text):
    for old, new in PATH_REPLACEMENTS.items():
        text = re.sub(rf'(?<!\\w){re.escape(old)}', new, text)
    return text

def update_file_paths_in_project(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.json', '.yml', '.yaml')):
                full_path = os.path.join(subdir, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    new_content = update_paths_in_text(content)
                    if new_content != content:
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        logging.info(f"Updated paths in {full_path}")
                except Exception as e:
                    logging.warning(f"Failed to update {full_path}: {e}")

def main():
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, filemode='w')
    logging.info("Migration started")

    for src_rel, dest_rel in MAPPING.items():
        src_path = os.path.join(SOURCE_DIR, src_rel)
        dest_path = os.path.join(SOURCE_DIR, dest_rel, os.path.basename(src_rel.rstrip('/')))

        if os.path.exists(src_path):
            try:
                move_item(src_path, dest_path)
                logging.info(f"MOVED: {src_rel} → {dest_rel}")
            except Exception as e:
                logging.error(f"ERROR moving {src_rel}: {e}")
        else:
            logging.warning(f"NOT FOUND: {src_rel}")

    remove_empty_dirs(SOURCE_DIR)
    update_file_paths_in_project(SOURCE_DIR)
    logging.info("Migration complete")

if __name__ == "__main__":
    main()

