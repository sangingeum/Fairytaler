from AppGUI import *
from AppModel import *
from tkinter import messagebox, filedialog

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
        self.view.set_image_prev_button_listener(self.image_prev)
        self.view.set_image_next_button_listener(self.image_next)
        self.view.set_music_prev_button_listener(self.music_prev)
        self.view.set_music_next_button_listener(self.music_next)
        self.view.set_music_play_button_listener(self.music_play)
        self.view.update_function = self.music_progress_bar_update

    def save(self):
        self.view.disable_all_buttons()
        self.model.save()
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
            self.music_first()


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

    def _new_game_helper(self, information):
        text, context_1, context_2 = self.model.new_game(*information)
        self._sync_main_text()
        # create images
        threading.Thread(target=self._create_and_replace_image, args=(context_1,)).start()
        threading.Thread(target=self._create_and_replace_image, args=(context_2,)).start()
        # create sound
        threading.Thread(target=self._create_and_save_music, args=(text,)).start()
        self._enable_all_buttons()

    def send(self):
        self.view.disable_all_buttons()
        user_prompt = self.view.user_textbox.get("0.0", "end").strip()
        if user_prompt != "":
            threading.Thread(target=self._send_helper, args=(user_prompt,)).start()
        else:
            self.view.enable_all_buttons()


    def _send_helper(self, user_prompt):
        if self.model.waiting_user_input:
            self._empty_user_textbox()
            self._sync_main_text()
        answer = self.model.process_user_text(user_prompt)
        if answer is not None:
            # create image and sound
            threading.Thread(target=self._create_and_replace_image, args=(answer,)).start()
            threading.Thread(target=self._create_and_save_music, args=(answer,)).start()
            self._sync_main_text()
        self._enable_all_buttons()

    def _create_and_replace_image(self, context):
        index = self.model.create_and_save_image(context)
        self.view.update_queue.put({"function": self.view.replace_image,
                                    "arg": self.model.get_image(index)})

    def music_progress_bar_update(self):
        # progress bar update
        progress = 0 if self.model.mixer.get_pos() == -1 else (self.model.mixer.get_pos() / 1000.0 / self.model.music_length)
        self.view.update_queue.put({"function": self.view.change_progress_bar_value, "arg": progress})
        # auto play next sound
        for event in pygame.event.get():
            if event.type == self.model.MUSIC_END:
                if self.view.music_keep_playing_toggle.get():
                    print('auto play next music')
                    self.music_next()
                    self.music_play()
                else:
                    self._change_music_play_button_label("▶")

    def _create_and_save_music(self, text):
        self.model.create_and_save_music(text)

    def _sync_main_text(self):
        self.view.update_queue.put({"function": self.view.replace_main_text, "arg": self.model.main_text})

    def _empty_user_textbox(self):
        self.view.update_queue.put({"function": self.view.empty_user_textbox})

    def _enable_all_buttons(self):
        self.view.update_queue.put({"function": self.view.enable_all_buttons})

    def _change_music_label(self, text):
        self.view.update_queue.put({"function": self.view.change_music_label, "arg": text})

    def _change_music_play_button_label(self, text):
        self.view.update_queue.put({"function": self.view.change_music_play_button_label, "arg": text})

    def image_prev(self):
        self.view.disable_all_buttons()
        image = self.model.get_prev_image()
        if image is not None:
            self.view.replace_image(image)
        self.view.enable_all_buttons()

    def image_next(self):
        self.view.disable_all_buttons()
        image = self.model.get_next_image()
        if image is not None:
            self.view.replace_image(image)
        self.view.enable_all_buttons()

    def music_prev(self):
        self.view.disable_all_buttons()
        success, index = self.model.load_prev_music()
        if success:
            self._change_music_label(f"Status: Playing {index}.wav")
            self._change_music_play_button_label("▶")
        self.view.enable_all_buttons()

    def music_play(self):
        self.view.disable_all_buttons()
        flag, index = self.model.play_music()
        if flag == "load":
            self._change_music_label(f"Status: Playing {index}.wav")
            self._change_music_play_button_label("=")
        elif flag == "unpause":
            self._change_music_play_button_label("=")
        elif flag == "pause":
            self._change_music_play_button_label("▶")
        self.view.enable_all_buttons()

    def music_next(self):
        self.view.disable_all_buttons()
        success, index = self.model.load_next_music()
        if success:
            self._change_music_label(f"Status: Playing {index}.wav")
            self._change_music_play_button_label("▶")
        self.view.enable_all_buttons()

    def music_first(self):
        self.view.disable_all_buttons()
        success, index = self.model.load_first_music()
        if success:
            self._change_music_label(f"Status: Playing {index}.wav")
        self.view.enable_all_buttons()