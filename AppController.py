from AppGUI import *
from AppModel import *


class AppController():
    def __init__(self, view: AppGUI, model: AppModel):
        self.view = view
        self.model = model
        self.init_view()

    def init_view(self):
        self.view.set_save_button_listener(self.save)
        self.view.set_load_button_listener(self.load)
        self.view.set_new_game_button_listener(self.new_game)
        self.view.set_send_button_listener(self.send)
        self.view.set_prev_button_listener(self.prev)
        self.view.set_next_button_listener(self.next)

    def save(self):
        self.view.disable_all_buttons()
        dialog = customtkinter.CTkInputDialog(text="Enter file name", title="Save")
        user_input = dialog.get_input()
        if user_input is not None:
            if user_input == "":
                messagebox.showinfo(title="Error", message="invalid file name")
            else:
                # remove spaces, add extension name
                user_input = user_input.replace(" ", "").replace(".", "") + ".sav"
                file_path = os.path.join(self.view.save_path, user_input)
                if os.path.isfile(file_path):
                    confirm_override = messagebox.askyesno(title="Override File",
                                                           message=f"'{user_input}' already exists. Do you want to override it?")
                    if confirm_override:
                        if not self.model.save(file_path):
                            messagebox.showinfo(title="Error", message="Nothing to save")
                else:
                    if not self.model.save(file_path):
                        messagebox.showinfo(title="Error", message="Nothing to save")
        self.view.enable_all_buttons()

    def load(self):
        self.view.disable_all_buttons()
        filetypes = (
            ('Save files', '*.sav'),
            ('All files', '*.*')
        )
        file_path = filedialog.askopenfilename(title="Load",
                                               initialdir=self.view.save_path,
                                               filetypes=filetypes)
        if self.model.load(file_path):
            self.view.replace_main_text(self.model.main_text)
            self.view.replace_image(self.model.get_last_image())

        self.view.enable_all_buttons()

    def new_game(self):
        self.view.disable_all_buttons()
        dialog = NewGameDialog(self.view)
        dialog.mainloop()
        if dialog.confirm:
            information = dialog.get_entered_information()
            threading.Thread(target=self._new_game_helper, args=(information,)).start()
        else:
            self.view.enable_all_buttons()
        dialog.destroy()

    def send(self):
        self.view.disable_all_buttons()
        user_prompt = self.view.user_textbox.get("0.0", "end").strip()
        if user_prompt != "":
            threading.Thread(target=self._send_helper, args=(user_prompt,)).start()
        else:
            self.view.enable_all_buttons()

    def prev(self):
        self.view.disable_all_buttons()
        image = self.model.get_prev_image()
        if image is not None:
            self.view.replace_image(image)
        self.view.enable_all_buttons()

    def next(self):
        self.view.disable_all_buttons()
        image = self.model.get_next_image()
        if image is not None:
            self.view.replace_image(image)
        self.view.enable_all_buttons()

    def _new_game_helper(self, information):
        text, context_1, context_2 = self.model.new_game(*information)
        self._replace_main_text(text)
        # create images
        threading.Thread(target=self._create_and_replace_image, args=(context_1,)).start()
        threading.Thread(target=self._create_and_replace_image, args=(context_2,)).start()
        self._enable_all_buttons()

    def _send_helper(self, user_prompt):
        if self.model.waiting_user_input:
            self._append_to_main_text("\n\n" + user_prompt)
            self._empty_user_textbox()
        answer = self.model.process_user_text(user_prompt)
        if answer is not None:
            threading.Thread(target=self._create_and_replace_image, args=(answer,)).start()
            self._append_to_main_text("\n\n" + answer)
        self._enable_all_buttons()

    def _create_and_replace_image(self, context):
        self.model.create_image_and_append(context)
        self.view.update_queue.put({"function": self.view.replace_image,
                                    "arg": self.model.get_last_image()})

    def _replace_main_text(self, text):
        self.view.update_queue.put({"function": self.view.replace_main_text, "arg": text})

    def _append_to_main_text(self, text):
        self.view.update_queue.put({"function": self.view.append_to_main_text, "arg": text})

    def _empty_user_textbox(self):
        self.view.update_queue.put({"function": self.view.empty_user_textbox})

    def _enable_all_buttons(self):
        self.view.update_queue.put({"function": self.view.enable_all_buttons})


if __name__ == "__main__":
    model = AppModel()
    view = AppGUI(model)
    AppController(view, model)
    view.mainloop()
