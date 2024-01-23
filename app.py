import controller
from tkinter import *
import customtkinter as ctk
from ttkwidgets.autocomplete import AutocompleteEntry

CHAMPION_IDS = controller.load_json('champion_ids.json')
ITEMS_IDS = controller.load_json('item_ids.json')
	
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Best Build Finder")
        #self.geometry(f"{400}x{500}")
        self.resizable(False, False)

        self.bind('<Return>', self.get_build)
        
        self.grid_columnconfigure(0, weight=1)

        self.champion_name = None
        self.matches_number = None
        self.depth = 1

        # FRAMES
        self.search_frame = ctk.CTkFrame(self, corner_radius=0)
        self.search_frame.grid(row=0, column=0, sticky='ew', columnspan = 2)

        self.champion_frame = ctk.CTkFrame(self, corner_radius=0)
        self.champion_frame.grid(row=1, column=0, sticky='nsew')

        self.build_frame = ctk.CTkFrame(self, corner_radius=0)
        self.build_frame.grid(row=1, column=1, sticky='nsew')

        self.build_label_frame = ctk.CTkFrame(self, corner_radius=0)
        self.build_label_frame.grid(row=2, column=0, sticky='nsew', columnspan = 2)

        # SEARCH FRAME WIDGETS
        self.champion_name_entry = AutocompleteEntry(self.search_frame, width = 15, font = ('Open Sans', 16), completevalues=CHAMPION_IDS.keys())
        self.champion_name_entry.grid(row=0, column=0, padx=15, pady=20, sticky = "ew")
        
        self.get_build_button =  ctk.CTkButton(self.search_frame, text = "Get Build", font = ('Open Sans', 20), command = self.get_build)
        self.get_build_button.grid(row=0, column=1, padx=15, pady=20, sticky = "ew")

        self.search_depth = ctk.CTkComboBox(self.search_frame, values=["20", "40", "60", "80", "100"], width = 75, state = "readonly", command=self.combobox_callback)
        self.search_depth.grid(row=0, column=2, padx=15, pady=20, sticky = "ew")
        self.search_depth.set("20")


    def get_build(self, *args):
        self.clear_frame(self.champion_frame)
        self.clear_frame(self.build_frame)
        self.clear_frame(self.build_label_frame)
        
        self.champion_name = self.champion_name_entry.get()

        matches = controller.get_matches(depth=self.depth, champion_id=int(CHAMPION_IDS[self.champion_name]))
        top_items = controller.get_items_count(matches=matches, items_dict=ITEMS_IDS)

        champion_image = controller.get_champion_image(self.champion_name)
        self.buttom_image = ctk.CTkButton(self.champion_frame, state=DISABLED, text="", fg_color = 'transparent', image=champion_image)
        self.buttom_image.grid(row=0, column=0)

        build_image = controller.get_build_image(top_items, ITEMS_IDS)
        self.buttom_image = ctk.CTkButton(self.build_frame, state=DISABLED, text="", fg_color = 'transparent', image=build_image)
        self.buttom_image.grid(row=0, column=0)

        ctk.CTkLabel(self.build_label_frame, text = f"Best items for : {self.champion_name}", font=('Open Sans', 20, 'bold'), justify = 'left').grid(row = 0, column=0, columnspan=2, padx = 5, pady = 5, sticky = "w")
        
        for idx, item in enumerate(list(top_items.keys())[:6]):
            ctk.CTkLabel(self.build_label_frame, text = f"- {item}", font=('Open Sans', 18, 'bold'), justify = 'left').grid(row = idx+1, column=0, columnspan=2, padx = 5, pady = 1, sticky = "w")

    def combobox_callback(self, choice):
        self.depth = int(int(choice) / 20)

    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()

