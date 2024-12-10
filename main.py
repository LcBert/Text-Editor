from tkinter import *
from tkinter import ttk, filedialog, messagebox
from typing import Literal
import subprocess
import json

import menu_bar

app: Tk = None


class App(Tk):

    def __init__(self):
        super().__init__()

        self.file = None
        self.filetypes = [
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        self.lang_type = f"{json.load(open("settings.json")).get("app_lang")}.json"
        self.lang_dict = json.load(open(f"lang/{self.lang_type}"))

        self.title("Text Editor")
        self.geometry("600x400")
        self.iconbitmap("img/appicon.ico")

        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        menu_bar.create_menu(self, self.lang_dict)

        self.editor_entry = Text(
            self,
            font="Consolas 12",
            wrap="word",
            undo=True,
            insertofftime=400,
            insertontime=900
        )
        self.editor_entry.grid(column=0, row=0, sticky="nsew")
        self.editor_entry.focus()
        self.editor_entry_scrollbar = Scrollbar(
            self,
            orient="vertical",
            jump=1
        )
        self.editor_entry_scrollbar.grid(column=1, row=0, sticky="ns")
        self.editor_entry_scrollbar.config(command=self.editor_entry.yview)
        self.editor_entry.config(yscrollcommand=self.editor_entry_scrollbar.set)

        ttk.Separator(self, orient="horizontal").grid(column=0, row=1, sticky="ew", columnspan=2)

        self.status_frame = Frame(self, height=20, borderwidth=1)
        self.status_frame.grid(column=0, row=2, sticky="ew")

        self.status_label = Label(self.status_frame, width=50, anchor="w")
        self.status_label.grid(column=0, row=0, sticky="w")

    def change_language(self, lang: str):
        with open("settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            settings["app_lang"] = lang
        with open("settings.json", "w") as settings_file:
            settings_file.write(json.dumps(settings))

        self.restart()

    def edit_wrap_content(self, wrap_mode: Literal["word", "char", "none"]):
        self.editor_entry.config(wrap=wrap_mode)

    def open_file(self):
        opened_file = filedialog.askopenfile(filetypes=self.filetypes, mode="r")
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
        self.destroy()
        global app
        app = App()
        app.start()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
