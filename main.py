from tkinter import *
from tkinter import ttk, filedialog, messagebox
from typing import Literal
import os
import sys
import subprocess
import json
import webbrowser

import menu_bar
import editor_entry
import status_frame

app: Tk = None


class App(Tk):
    def __init__(self, file=None):
        super().__init__()

        self.filetypes = [
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]

        if getattr(sys, "frozen", False):
            os.chdir(os.path.dirname(os.path.abspath(sys.executable)))

        self.load_settings(file=file)

        self.title("Text Editor" + (" - " + self.file.name.split("/")[-1] if self.file is not None else ""))
        self.geometry("920x512+100+100")
        self.iconbitmap("img/appicon.ico")
        self.protocol("WM_DELETE_WINDOW", self.xquit)  # Handle exit with X window button

        # Key bindings
        self.bind("<Control-n>", lambda event: self.clear_app())  # Control + N -> New File
        self.bind("<Control-N>", lambda event: self.new_window())  # Control + Shift + N -> New Window
        self.bind("<Control-o>", lambda event: self.open_file())  # Control + O -> Open File
        self.bind("<Control-s>", lambda event: self.save_file())  # Control + S -> Save File
        self.bind("<Control-S>", lambda event: self.save_as_file())  # Control + Shift + S -> Save File As
        self.bind("<Control-q>", lambda event: self.close_file())  # Control + Q -> Close File
        self.bind("<Control-e>", lambda event: self.show_in_explorer())  # Control + E -> Show in Explorer
        self.bind("<Control-w>", lambda event: self.xquit())  # Control + W -> Quit Application

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_widgets()
        self.add_file_to_recent_files(file=file)

    # Load Settings File #
    def load_settings(self, file=None, wrap_mode: Literal["word", "char", "none"] = "word", text: str = ""):
        self.file = file
        self.wrap_mode = wrap_mode
        if (self.file is not None):
            with (open(self.file.name, "r")) as file:
                self.text = file.read()
        else:
            self.text = text
        with open("settings.json", "r") as settings_file:
            file_dict: dict = json.load(settings_file)
            self.lang_dict = json.load(open(f"lang/{file_dict.get("app.lang")}.json"))
            self.language = file_dict.get("app.lang")
            self.font = file_dict.get("app.font")

    def create_widgets(self):
        menu_bar.create_menu(self)
        editor_entry.create_editor_entry(self)
        ttk.Separator(self, orient="horizontal").grid(column=0, row=1, sticky="ew", columnspan=2)
        status_frame.create_status_frame(self)

    def change_language(self, lang: str):
        with open("settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            settings["app.lang"] = lang
        with open("settings.json", "w") as settings_file:
            settings_file.write(json.dumps(settings))
        self.restart()

    def edit_wrap_content(self, wrap_mode: Literal["word", "char", "none"]):
        self.editor_entry.config(wrap=wrap_mode)
        self.status_wrap_mode_label.config(text=f"Wrap mode: {wrap_mode.capitalize()}")

    def clear_app(self):
        self.editor_entry.delete("1.0", "end")
        self.file = None
        self.title("Text Editor")

    def new_window(self):
        subprocess.Popen(sys.argv[0])

    def open_file(self, args_file=None):
        if (args_file is None):
            opened_file = filedialog.askopenfile(filetypes=self.filetypes, mode="r")
        else:
            try:
                opened_file = open(args_file, "r")
            except FileNotFoundError:
                self.show_message_status_frame(self.lang_dict.get("editor.statusmessage.filenotfound"), "red")
                return
        if (opened_file is not None):
            self.file = opened_file
            self.title("Text Editor - " + self.file.name.split("/")[-1])
            self.editor_entry.delete("1.0", "end")
            self.editor_entry.insert("1.0", self.file.read())
            self.show_message_status_frame(self.lang_dict.get("editor.statusmessage.open") % self.file.name.split("/")[-1])
            self.add_file_to_recent_files(self.file)

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
            self.add_file_to_recent_files(self.file)

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
            self.show_message_status_frame(self.lang_dict.get("editor.statusmessage.nofileopen"), "red")

    def show_message_status_frame(self, message: str, color: str = "black"):
        self.status_message_label.config(text=message, fg=color)

    def add_file_to_recent_files(self, file=None):
        with open("settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            recent_files = settings.get("app.recent_files")
            if (file is not None):
                if (recent_files is None):
                    recent_files = []
                if (file.name not in recent_files):
                    recent_files.append(file.name)
                if (file.name in recent_files):
                    recent_files.remove(file.name)
                    recent_files.insert(0, file.name)
            settings["app.recent_files"] = recent_files
            while (len(recent_files) > 20):
                recent_files.pop()
        with open("settings.json", "w") as settings_file:
            settings_file.write(json.dumps(settings))
        menu_bar.refresh_recent_file_menu(self, recent_files)

    def clear_recent_file_list(self):
        with open("settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            settings["app.recent_files"] = []
        with open("settings.json", "w") as settings_file:
            settings_file.write(json.dumps(settings))
        menu_bar.refresh_recent_file_menu(self, [])

    def restart(self):
        file = self.file
        wrap_mode = self.editor_entry.cget("wrap")
        text = self.editor_entry.get("1.0", "end").strip()
        for child in self.winfo_children():
            child.destroy()
        self.load_settings(file, wrap_mode, text)
        self.create_widgets()
        self.add_file_to_recent_files()

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

    def open_link(self, link: str):
        # subprocess.Popen(f"start {link}")
        webbrowser.open(link)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_to_open = open(sys.argv[1].replace("\\", "/"))
        app = App(file_to_open)
        app.start()
        file_to_open.close()
    else:
        app = App()
        app.start()
