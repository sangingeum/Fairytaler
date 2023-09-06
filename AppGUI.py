import customtkinter
from PIL import Image
import os
class AppGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
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
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Save", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Load", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 10))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 20))

        # create user_textbox and button
        self.user_textbox = customtkinter.CTkTextbox(master=self, height=28, activate_scrollbars=True)
        self.user_textbox.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), text="Send")
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create story_textbox
        self.story_textbox = customtkinter.CTkTextbox(self, width=250, activate_scrollbars=True)
        self.story_textbox.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create checkbox and switch frame
        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.grid(row=0, column=2, columnspan=2, padx=(20, 20), pady=(20, 0), sticky="new")

        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "CustomTkinter_logo_single.png")), size=(512, 512))

        self.image_label = customtkinter.CTkLabel(self.image_frame, image=self.image, text="")
        self.image_label.grid(row=0, column=0, pady=(20, 0), padx=20, sticky="ne")


        # set default values
        self.appearance_mode_optionemenu.set("dark")
        self.scaling_optionemenu.set("100%")
        self.story_textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        self.image_label.configure(image=customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "large_test_image.png"))))


if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()
