import controller

ITEMS_IDS = controller.load_json('item_ids.json')

print(list(ITEMS_IDS.keys()))