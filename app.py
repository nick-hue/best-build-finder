import controller
import json

champion_name = "Mordekaiser"
number_of_matches = 20
depth = int(number_of_matches / 20) 

with open('champion_ids.json') as json_file:
    champion_ids = json.load(json_file)

with open('item_ids.json') as json_file:
    item_ids = json.load(json_file)
    
matches = controller.get_matches(depth=depth, champion_id=int(champion_ids[champion_name]))
top_items = controller.get_items_count(matches=matches, items_dict=item_ids)

print(f"Best items for: {champion_name}")
for item in list(top_items.keys())[:6]:
    print("- "+item)