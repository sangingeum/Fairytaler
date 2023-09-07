import os.path

import customtkinter
from PIL import Image
from AppModel import *
from customtkinter import filedialog
from tkinter import messagebox
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
        self.grid_rowconfigure((0, 1, 2), weight=1)
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1) # empty space at row 10
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Fairytaler", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        ## buttons
        self.save_button = customtkinter.CTkButton(self.sidebar_frame, text="Save", command=self._save_button_listener)
        self.save_button.grid(row=1, column=0, padx=20, pady=10)
        self.load_button = customtkinter.CTkButton(self.sidebar_frame, text="Load", command=self._load_button_listener)
        self.load_button.grid(row=2, column=0, padx=20, pady=10)
        self.new_game_button = customtkinter.CTkButton(self.sidebar_frame, text="New Game", command=self._new_game_button_listener)
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

        # set default values
        self.appearance_mode_optionemenu.set("dark")
        self.scaling_optionemenu.set("100%")
        self.main_textbox.configure(state="disabled")
        # set paths
        self.save_path = os.path.join(self.current_path, "saves")

    def _change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    def _change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def _replace_main_text(self, text):
        self.main_textbox.configure(state="normal")
        self.main_textbox.delete("0.0", "end")
        self.main_textbox.insert("0.0", text)
        self.main_textbox.configure(state="disabled")

    def _replace_image(self, image):
        self.image_label.configure(image=customtkinter.CTkImage(image, size=(512, 512)))
    def _disable_all_buttons(self):
        self.send_button.configure(state="disabled")
        self.load_button.configure(state="disabled")
        self.new_game_button.configure(state="disabled")
        self.save_button.configure(state="disabled")

    def _enable_all_buttons(self):
        self.send_button.configure(state="normal")
        self.load_button.configure(state="normal")
        self.new_game_button.configure(state="normal")
        self.save_button.configure(state="normal")
    def _save_button_listener(self):
        self._disable_all_buttons()
        dialog = customtkinter.CTkInputDialog(text="Enter file name", title="Save")
        user_input = dialog.get_input()
        if user_input is not None:
            if user_input == "":
                messagebox.showinfo(title="Error", message="invalid file name")
            else:
                # remove spaces, add extension name
                user_input = user_input.replace(" ", "").replace(".", "") + ".sav"
                file_path = os.path.join(self.save_path, user_input)
                if os.path.isfile(file_path):
                    confirm_override = messagebox.askyesno(title="Override File", message=f"'{user_input}' already exists. Do you want to override it?")
                    if confirm_override:
                        if not self.model.save(file_path):
                            messagebox.showinfo(title="Error", message="Nothing to save")
                else:
                    if not self.model.save(file_path):
                        messagebox.showinfo(title="Error", message="Nothing to save")
        self._enable_all_buttons()
    def _load_button_listener(self):
        self._disable_all_buttons()
        filetypes = (
            ('Save files', '*.sav'),
            ('All files', '*.*')
        )
        file_path = filedialog.askopenfilename(title="Load",
                                               initialdir=self.save_path,
                                               filetypes=filetypes)
        if self.model.load(file_path):
            self._replace_main_text(self.model.main_text)
            self._replace_image(self.model.images[-1])
        self._enable_all_buttons()
    def _new_game_button_listener(self):
        self._disable_all_buttons()
        dialog = NewGameDialog(self)
        dialog.mainloop()
        text = None
        context_1 = None
        context_2 = None
        if dialog.confirm:
            information = dialog.get_entered_information()
            dialog.destroy()
            text, context_1, context_2 = self.model.new_game(*information)
        dialog.destroy()
        self._enable_all_buttons()
        if text is not None:
            self._replace_main_text(text)
            # create images
            image_1 = self.model.create_image_and_append(context_1)
            self._replace_image(image_1)
            image_2 = self.model.create_image_and_append(context_2)
            self._replace_image(image_2)

    def _send_button_listener(self):
        self._disable_all_buttons()
        print("send")
        self._enable_all_buttons()

    def _exit_button_listener(self):
        self._disable_all_buttons()
        self.model.exit()
        self.destroy()
        self._enable_all_buttons()


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
        self.universe_entry = customtkinter.CTkEntry(self.frame,
                                                     placeholder_text="Describe the universe you want to explore")

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

        self.confirm_button = customtkinter.CTkButton(self.frame, command=self._confirm_button_clicked
                                                      , text="Confirm")
        self.cancel_button = customtkinter.CTkButton(self.frame, command=self._cancel_button_clicked
                                                     , text="Cancel")

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
