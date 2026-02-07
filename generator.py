import os
import sys
import yaml

# --- KONFIGURATION & PRESETS ---
# Hier kannst du fertige GUIs definieren, die man einfach auswählen kann.
PRESETS = {
    "standard_shop": {
        "title": "§8» §6__Shop__",
        "rows": 6,
        "items": {
            "border": {
                "item": "minecraft:black_stained_glass_pane",
                "slots": [0, 1, 2, 3, 4, 5, 6, 7, 8, 45, 46, 47, 48, 49, 50, 51, 52, 53]
            },
            "close_button": {
                "item": "minecraft:barrier",
                "slot": 49,
                "display_name": "§cSchließen",
                "actions": {"click": ["close"]}
            }
        }
    },
    "warp_menu": {
        "title": "§8» §9Warp Menü",
        "rows": 3,
        "items": {
            "spawn": {
                "item": "minecraft:nether_star",
                "slot": 13,
                "display_name": "§aSpawn",
                "actions": {"click": ["console: warp spawn %player%"]}
            }
        }
    }
}

class IAGenerator:
    def __init__(self, namespace):
        self.namespace = namespace
        self.base_path = f"contents/{namespace}/configs"
        # Erstellt die Ordnerstruktur automatisch
        os.makedirs(self.base_path, exist_ok=True)

    def create_gui(self, gui_id, title, rows, items_map, texture_id=None):
        # Falls eine Textur-ID angegeben ist, wird sie als Font-Image eingebaut
        title_string = title
        if texture_id:
            # Standard IA Offset für Vollbild-GUIs ist meist -16
            title_string = f":offset_-16:%font_image:{self.namespace}:{texture_id}%§r{title}"

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
            yaml.dump(gui_config, f, sort_keys=False, allow_unicode=True, default_flow_style=False)
        
        print(f"✅ Datei generiert: {file_path}")

def main():
    # Erkennung ob das Skript auf GitHub Actions läuft (vermeidet EOF-Error)
    is_github = "GITHUB_ACTIONS" in os.environ or "--auto" in sys.argv

    if is_github:
        print("🤖 GitHub Modus: Generiere Standard-Presets...")
        gen = IAGenerator("custom_gui")
        # Generiert automatisch alle Presets für das Repo
        for name, data in PRESETS.items():
            gen.create_gui(name, data["title"], data["rows"], data["items"])
    else:
        print("--- 🛠️ ItemAdder GUI Generator ---")
        ns = input("Namespace [mein_server]: ") or "mein_server"
        gen = IAGenerator(ns)

        print("\nVerfügbare Optionen:")
        print("[1] Ein fertiges Preset nutzen")
        print("[2] Ganz neu erstellen")
        
        wahl = input("\nDeine Wahl: ")

        if wahl == "1":
            print("\nPresets:", ", ".join(PRESETS.keys()))
            p_name = input("Welches Preset? ")
            if p_name in PRESETS:
                p = PRESETS[p_name]
                gen.create_gui(p_name, p["title"], p["rows"], p["items"])
            else:
                print("❌ Preset nicht gefunden.")
        
        elif wahl == "2":
            g_id = input("GUI ID (Dateiname): ")
            g_title = input("Titel im Spiel: ")
            g_rows = int(input("Reihen (1-6): "))
            gen.create_gui(g_id, g_title, g_rows, {})

if __name__ == "__main__":
    main()
