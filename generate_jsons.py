import controller
import os

if not os.path.exists("champion_ids.json"):
    controller.get_champion_ids_json()

if not os.path.exists("item_ids.json"):
    controller.get_item_ids_to_json()
