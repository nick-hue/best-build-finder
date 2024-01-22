import controller
from tkinter import *
import customtkinter as ctk

champion_name = "Akshan"
number_of_matches = 20
depth = int(number_of_matches / 20) 

champion_ids = controller.load_json('champion_ids.json')
item_ids = controller.load_json('item_ids.json')

matches = controller.get_matches(depth=depth, champion_id=int(champion_ids[champion_name]))
top_items = controller.get_items_count(matches=matches, items_dict=item_ids)

print(f"Best items for: {champion_name}")
for item in list(top_items.keys())[:6]:
    print("- "+item)
	

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Best Build Finder")
        self.geometry(f"{1100}x{580}")

        



if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()

