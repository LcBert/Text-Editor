from tkinter import *
from tkinter import ttk
import json


def __file_menu(app: Tk, menubar: Menu, lang: dict) -> Menu:
    file_menu = Menu(menubar, tearoff=0)

    # file_menu.add_command(label="Open", command=app.open_file)
    file_menu.add_command(label=lang.get("menubar.file.open"), command=app.open_file)
    file_menu.add_command(label=lang.get("menubar.file.save"), command=app.save_file)
    file_menu.add_command(label=lang.get("menubar.file.saveas"), command=app.save_as_file)
    file_menu.add_command(label=lang.get("menubar.file.close"), command=app.close_file)
    file_menu.add_separator()
    file_menu.add_command(label=lang.get("menubar.file.explorer"), command=app.show_in_explorer)
    file_menu.add_separator()
    file_menu.add_command(label=lang.get("menubar.file.exit"), command=app.quit)

    return file_menu


def __format_menu(app: Tk, menubar: Menu, lang: dict) -> Menu:
    format_menu = Menu(menubar, tearoff=0)

    format_wrap_submenu = Menu(format_menu, tearoff=0)
    format_wrap_submenu.add_command(label=lang.get("menubar.format.wrap.word"), command=lambda: app.edit_wrap_content("word"))
    format_wrap_submenu.add_command(label=lang.get("menubar.format.wrap.char"), command=lambda: app.edit_wrap_content("char"))
    format_wrap_submenu.add_command(label=lang.get("menubar.format.wrap.none"), command=lambda: app.edit_wrap_content("none"))

    format_language_submenu = Menu(format_menu, tearoff=0)
    format_language_submenu.add_command(label="English", command=lambda: app.change_language("en"))
    format_language_submenu.add_command(label="Italiano", command=lambda: app.change_language("it"))
    format_language_submenu.add_command(label="Español", command=lambda: app.change_language("sp"))

    format_menu.add_cascade(label=lang.get("menubar.format.wrap"), menu=format_wrap_submenu)
    format_menu.add_cascade(label=lang.get("menubar.format.language"), menu=format_language_submenu)

    return format_menu


def create_menu(app: Tk, lang: dict):

    menubar = Menu(app)
    app.config(menu=menubar)

    menubar.add_cascade(label=lang.get("menubar.file"), menu=__file_menu(app, menubar, lang))
    menubar.add_cascade(label=lang.get("menubar.format"), menu=__format_menu(app, menubar, lang))
