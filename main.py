from tkinter import *
from tkinter import ttk, filedialog, messagebox
from typing import Literal
import subprocess
import json

import menu_bar
import editor_entry
import status_frame

app: Tk = None


class App(Tk):
    def __init__(self):
        super().__init__()

        self.file = None
        self.filetypes = [
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        self.wrap_mode = "word"
        self.text = ""

        self.load_settings()

        self.title("Text Editor" + (" - " + self.file.name.split("/")[-1] if self.file is not None else ""))
        self.geometry("600x400+100+100")
        self.iconbitmap("img/appicon.ico")
        self.protocol("WM_DELETE_WINDOW", self.xquit)  # Handle exit with X window button

        self.bind("<Control-o>", lambda event: self.open_file())  # Control + O -> Open File
        self.bind("<Control-s>", lambda event: self.save_file())  # Control + S -> Save File
        self.bind("<Control-S>", lambda event: self.save_as_file())  # Control + Shift + S -> Save File
        self.bind("<Control-q>", lambda event: self.close_file())  # Control + Q -> Close File
        self.bind("<Control-e>", lambda event: self.show_in_explorer())  # Control + E -> Show in Explorer

        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.create_widgets()

    # Load Settings File #
    def load_settings(self, file=None, wrap_mode: Literal["word", "char", "none"] = "word", text: str = ""):
        self.file = file
        self.wrap_mode = wrap_mode
        self.text = text
        with open("settings.json", "r") as settings_file:
            file_dict: dict = json.load(settings_file)
            self.lang_dict = json.load(open(f"lang/{file_dict.get("app.lang")}.json"))
            self.font = file_dict.get("app.font")

    def create_widgets(self):
        self.menubar: Menu = menu_bar.create_menu(self)
        self.editor_entry, self.editor_entry_scrollbar = editor_entry.create_editor_entry(self)
        ttk.Separator(self, orient="horizontal").grid(column=0, row=1, sticky="ew", columnspan=2)
        self.status_frame, self.status_label = status_frame.create_status_frame(self)

    def change_language(self, lang: str):
        with open("settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            settings["app.lang"] = lang
        with open("settings.json", "w") as settings_file:
            settings_file.write(json.dumps(settings))
        self.restart()

    def edit_wrap_content(self, wrap_mode: Literal["word", "char", "none"]):
        self.editor_entry.config(wrap=wrap_mode)

    def open_file(self, args_file=None):
        if (args_file is None):
            opened_file = filedialog.askopenfile(filetypes=self.filetypes, mode="r")
        else:
            opened_file = open(args_file, "r")
        if (opened_file is not None):
            self.file = opened_file
            self.title("Text Editor - " + self.file.name.split("/")[-1])
            self.editor_entry.delete("1.0", "end")
            self.editor_entry.insert("1.0", self.file.read())
            self.show_message_status_frame(self.lang_dict.get("editor.statusmessage.open") % self.file.name.split("/")[-1])

    def save_file(self):
        text = self.editor_entry.get("1.0", "end").strip()
        if (self.file is not None):
            self.file = open(self.file.name, "w")
            self.file.write(text)
            self.file.flush()
            self.show_message_status_frame(self.lang_dict.get("editor.statusmessage.save") % self.file.name.split("/")[-1])
        else:
            self.save_as_file()

    def save_as_file(self):
        text = self.editor_entry.get("1.0", "end").strip()
        opened_file = filedialog.asksaveasfile(filetypes=self.filetypes, defaultextension=".txt")
        if (opened_file is not None):
            self.file = opened_file
            self.title("Text Editor - " + self.file.name.split("/")[-1])
            self.file.write(text)
            self.file.flush()
            self.show_message_status_frame(self.lang_dict.get("editor.statusmessage.save") % self.file.name.split("/")[-1])

    def close_file(self):
        if (self.file is not None):
            self.show_message_status_frame(f"File {self.file.name.split("/")[-1]} closed")
            self.editor_entry.delete("1.0", "end")
            self.file.close()
            self.file = None
            self.title("Text Editor")

    def show_in_explorer(self):
        if (self.file is not None):
            subprocess.Popen(f'explorer /select,"{self.file.name.replace("/", "\\")}"')
        else:
            self.show_message_status_frame(self.lang_dict.get("editor.statusmessage.filenotfound"), "red")

    def show_message_status_frame(self, message: str, color: str = "black"):
        self.status_label.config(text=message, fg=color)

    def restart(self):
        file = self.file
        wrap_mode = self.editor_entry.cget("wrap")
        text = self.editor_entry.get("1.0", "end").strip()
        for child in self.winfo_children():
            child.destroy()
        self.load_settings(file, wrap_mode, text)
        self.create_widgets()

    def ask_save_on_exit(self):
        ask_exit: bool = messagebox.askyesnocancel("Text Editor", self.lang_dict.get("editor.exit.ask_save"))
        if (ask_exit is True):
            self.save_file()
            self.quit()
        elif (ask_exit is False):
            self.quit()

    def xquit(self):
        if (self.file is not None):
            with (open(self.file.name, "r")) as file:
                if (self.editor_entry.get("1.0", "end").strip() != file.read()):
                    self.ask_save_on_exit()
                else:
                    self.quit()
        elif (self.editor_entry.get("1.0", "end").strip() != ""):
            self.ask_save_on_exit()
        else:
            self.quit()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
