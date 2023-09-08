import os.path
import customtkinter
from PIL import Image
from AppModel import *
from customtkinter import filedialog
from tkinter import messagebox
from queue import Queue

class AppGUI(customtkinter.CTk):
    def __init__(self, model : AppModel):
        super().__init__()
        # set model
        self.model = model
        # set default style
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        # configure window
        self.title("Fairytaler")
        self.geometry(f"{1280}x{720}")
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=10000)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((1, 2), weight=1)
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1) # empty space at row 10
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Fairytaler", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        ## buttons
        self.save_button = customtkinter.CTkButton(self.sidebar_frame, text="Save", command=self._default_listener)
        self.save_button.grid(row=1, column=0, padx=20, pady=10)
        self.load_button = customtkinter.CTkButton(self.sidebar_frame, text="Load", command=self._default_listener)
        self.load_button.grid(row=2, column=0, padx=20, pady=10)
        self.new_game_button = customtkinter.CTkButton(self.sidebar_frame, text="New Game", command=self._default_listener)
        self.new_game_button.grid(row=3, column=0, padx=20, pady=10)
        ## options
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self._change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 10))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],command=self._change_scaling_event)
        self.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 20))
        # create user_textbox and send button
        self.user_textbox = customtkinter.CTkTextbox(master=self, height=28, activate_scrollbars=True)
        self.user_textbox.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.send_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), text="Send")
        self.send_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create main_textbox
        self.main_textbox = customtkinter.CTkTextbox(self, width=250, activate_scrollbars=True)
        self.main_textbox.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create checkbox and switch frame
        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.grid(row=0, column=2, columnspan=2, padx=(20, 20), pady=(20, 0), sticky="new")

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.image_path = os.path.join(self.current_path, "test_images")
        self.image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "CustomTkinter_logo_single.png")), size=(512, 512))

        self.image_label = customtkinter.CTkLabel(self.image_frame, image=self.image, text="")
        self.image_label.grid(row=0, column=0, pady=(20, 0), padx=20, sticky="ne")

        # image_change_buttons
        self.prev_button = customtkinter.CTkButton(self, text="Prev", command=self._default_listener)
        self.prev_button.grid(row=1, column=2, pady=(20, 0), padx=20, sticky="nw")
        self.next_button = customtkinter.CTkButton(self, text="Next", command=self._default_listener)
        self.next_button.grid(row=1, column=3, pady=(20, 0), padx=20, sticky="ne")

        # set default values
        self.appearance_mode_optionemenu.set("dark")
        self.scaling_optionemenu.set("100%")
        self.main_textbox.configure(state="disabled")
        # set paths
        self.save_path = os.path.join(self.current_path, "saves")
        # GUI update queue
        self.update_queue = Queue()
        self._periodic_update()

    def _periodic_update(self):
        self.after(200, func=self._periodic_update)
        self.apply_update()

    def _default_listener(self):
        print("default_listener")
    def _change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    def _change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def apply_update(self):
        while True:
            try:
                update = self.update_queue.get(block=False, timeout=None)
                self._process_update(update)
            except:
                break

    def _process_update(self, update):
        arg = update.get("arg")
        if arg is None:
            update["function"]()
        else:
            update["function"](arg)

    def replace_main_text(self, text):
        self.main_textbox.configure(state="normal")
        self.main_textbox.delete("0.0", "end")
        self.main_textbox.insert("0.0", text)
        self.main_textbox.configure(state="disabled")

    def append_to_main_text(self, text):
        self.main_textbox.configure(state="normal")
        self.main_textbox.insert("end", text)
        self.main_textbox.see("end")
        self.main_textbox.configure(state="disabled")

    def replace_image(self, image):
        self.image_label.configure(image=customtkinter.CTkImage(image, size=(512, 512)))

    def empty_user_textbox(self):
        self.user_textbox.delete("0.0", "end")

    def disable_all_buttons(self):
        self.send_button.configure(state="disabled")
        self.load_button.configure(state="disabled")
        self.new_game_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.prev_button.configure(state="disabled")
        self.next_button.configure(state="disabled")

    def enable_all_buttons(self):
        self.send_button.configure(state="normal")
        self.load_button.configure(state="normal")
        self.new_game_button.configure(state="normal")
        self.save_button.configure(state="normal")
        self.prev_button.configure(state="normal")
        self.next_button.configure(state="normal")

    def set_save_button_listener(self, command):
        self.save_button.configure(command=command)
    def set_load_button_listener(self, command):
        self.load_button.configure(command=command)
    def set_new_game_button_listener(self, command):
        self.new_game_button.configure(command=command)
    def set_send_button_listener(self, command):
        self.send_button.configure(command=command)

    def set_prev_button_listener(self, command):
        self.prev_button.configure(command=command)

    def set_next_button_listener(self, command):
        self.next_button.configure(command=command)

# NewGameDialog is popped up when the new game button is clicked
class NewGameDialog(customtkinter.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.confirm = False
        self.title("New game")
        self.geometry("500x500")
        self.frame = customtkinter.CTkFrame(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # override x button
        self.protocol('WM_DELETE_WINDOW', self._cancel_button_clicked)

        self.frame.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")

        self.universe_label = customtkinter.CTkLabel(self.frame, text="Universe")
        self.universe_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Describe the universe you want to explore")

        self.name_label = customtkinter.CTkLabel(self.frame, text="Name")
        self.name_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Enter your name")

        self.gender_label = customtkinter.CTkLabel(self.frame, text="Gender")
        self.gender_checkbox = customtkinter.CTkCheckBox(self.frame, text="Male")

        self.race_label = customtkinter.CTkLabel(self.frame, text="Race")
        self.race_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Enter your race")

        self.personality_label = customtkinter.CTkLabel(self.frame, text="Personality")
        self.personality_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Enter your personality")

        self.bg_label = customtkinter.CTkLabel(self.frame, text="Background")
        self.bg_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Enter your background")

        self.confirm_button = customtkinter.CTkButton(self.frame, command=self._confirm_button_clicked, text="Confirm")
        self.cancel_button = customtkinter.CTkButton(self.frame, command=self._cancel_button_clicked, text="Cancel")

        ### grid setting
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 20), weight=1)
        self.frame.grid_rowconfigure(10, weight=100)
        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid_columnconfigure(2, weight=2)

        self.universe_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.universe_entry.grid(row=0, column=1, columnspan=2, padx=20, pady=(10, 10), sticky="nsew")
        self.name_label.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.name_entry.grid(row=1, column=1, columnspan=2, padx=20, pady=(10, 10), sticky="nsew")
        self.gender_label.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.gender_checkbox.grid(row=2, column=1, columnspan=2, padx=20, pady=(10, 10), sticky="nsew")
        self.race_label.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.race_entry.grid(row=3, column=1, columnspan=2, padx=20, pady=(10, 10), sticky="nsew")
        self.personality_label.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.personality_entry.grid(row=4, column=1, columnspan=2, padx=20, pady=(10, 10), sticky="nsew")
        self.bg_label.grid(row=5, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.bg_entry.grid(row=5, column=1, columnspan=2, padx=20, pady=(10, 10), sticky="nsew")

        self.confirm_button.grid(row=20, column=0, columnspan=2, padx=20, pady=(10, 10))
        self.cancel_button.grid(row=20, column=2, padx=20, pady=(10, 10))

        self.attributes('-topmost', 'true')
        self.grab_set()

    def _confirm_button_clicked(self):
        self.confirm = True
        self.quit()

    def _cancel_button_clicked(self):
        self.quit()

    def get_entered_information(self):
        # universe, name, gender, race, personality, background
        universe = self.universe_entry.get()
        name = self.name_entry.get()
        gender = "male" if self.gender_checkbox.get() == 1 else "female"
        race = self.race_entry.get()
        personality = self.personality_entry.get()
        background = self.bg_entry.get()
        return (universe, name, gender, race, personality, background)


if __name__ == "__main__":
    model = AppModel()
    app = AppGUI(model)
    app.mainloop()
