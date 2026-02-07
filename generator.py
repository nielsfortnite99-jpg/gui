import os
import yaml # Falls nicht installiert: pip install pyyaml

class IAGenerator:
    def __init__(self, namespace):
        self.namespace = namespace
        self.base_path = f"contents/{namespace}/configs"
        os.makedirs(self.base_path, exist_ok=True)

    def create_gui(self, gui_id, title, rows, items_map, texture_id=None):
        # Titel mit oder ohne Custom Texture Offset
        title_string = title
        if texture_id:
            title_string = f"%font_image:{self.namespace}:{texture_id}%§r {title}"

        gui_config = {
            "info": {"namespace": self.namespace},
            "guis": {
                gui_id: {
                    "title": title_string,
                    "type": "CHEST",
                    "rows": rows,
                    "static_items": items_map
                }
            }
        }

        file_path = os.path.join(self.base_path, f"{gui_id}.yml")
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(gui_config, f, sort_keys=False, allow_unicode=True)
        print(f"✅ GUI '{gui_id}' erstellt unter: {file_path}")

# --- PRESETS ---
PRESETS = {
    "basic_shop": {
        "title": "Item Shop",
        "rows": 3,
        "items": {
            "back_button": {"item": "minecraft:arrow", "slot": 18, "actions": {"click": ["close"]}},
            "border": {"item": "minecraft:black_stained_glass_pane", "slots": [0,1,2,3,4,5,6,7,8]}
        }
    }
}

def main():
    print("--- ItemAdder GUI Generator ---")
    namespace = input("Namespace [default]: ") or "default"
    gen = IAGenerator(namespace)

    mode = input("Wähle: [1] Preset laden, [2] Eigene GUI erstellen: ")

    if mode == "1":
        print("Verfügbare Presets:", list(PRESETS.keys()))
        choice = input("Name des Presets: ")
        if choice in PRESETS:
            p = PRESETS[choice]
            gen.create_gui(choice, p["title"], p["rows"], p["items"])
    
    elif mode == "2":
        name = input("GUI ID: ")
        rows = int(input("Anzahl Reihen (1-6): "))
        title = input("Anzeigename (Titel): ")
        # Hier könnten weitere Abfragen für Items folgen
        gen.create_gui(name, title, rows, {})

if __name__ == "__main__":
    main()
