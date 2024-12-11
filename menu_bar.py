from tkinter import *
from tkinter import ttk


def __file_menu(app: Tk, menubar: Menu, lang: dict) -> Menu:
    file_menu = Menu(menubar, tearoff=0)

    file_recent_submenu = Menu(file_menu, tearoff=0)
    # file_recent_submenu.add_command(label="file1.txt", command=lambda: app.open_file("file1.txt"))

    file_menu.add_command(label=lang.get("menubar.file.open"), command=app.open_file)
    file_menu.add_command(label=lang.get("menubar.file.save"), command=app.save_file)
    file_menu.add_command(label=lang.get("menubar.file.saveas"), command=app.save_as_file)
    file_menu.add_command(label=lang.get("menubar.file.close"), command=app.close_file)
    file_menu.add_separator()
    file_menu.add_command(label=lang.get("menubar.file.explorer"), command=app.show_in_explorer)
    file_menu.add_cascade(label=lang.get("menubar.file.recent"), menu=file_recent_submenu)
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


def __help_menu(app: Tk, menubar: Menu, lang: dict) -> Menu:
    help_menu = Menu(menubar, tearoff=0)

    help_menu.add_command(label=lang.get("menubar.help.about"), command=lambda: __help_show_about(app, lang))

    return help_menu


def create_menu(app: Tk, lang: dict) -> Menu:
    menubar = Menu(app)
    app.config(menu=menubar)

    menubar.add_cascade(label=lang.get("menubar.file"), menu=__file_menu(app, menubar, lang))
    menubar.add_cascade(label=lang.get("menubar.format"), menu=__format_menu(app, menubar, lang))
    menubar.add_cascade(label=lang.get("menubar.help"), menu=__help_menu(app, menubar, lang))

    return menubar


def __help_show_about(app: Tk, lang: dict):
    info_content = [
        "Version 1.0",
        "Author: Luca Bertaggia"
    ]
    about_window = Toplevel(app)
    about_window.title(lang.get("menubar.help.about"))
    about_window.geometry("300x150")
    about_window.resizable(False, False)
    about_window.wm_attributes("-toolwindow", True)
    about_window.wm_attributes("-topmost", True)

    about_window.grid_columnconfigure(0, weight=1)
    about_window.grid_rowconfigure(1, weight=1)

    title_frame = Frame(about_window)
    title_frame.grid(column=0, row=0, sticky="ew")

    appicon = PhotoImage(file="img/appicon.png")
    image_label = Label(title_frame, image=appicon)
    image_label.image = appicon  # keep a reference to the image
    image_label.grid(column=0, row=0)

    title_label = Label(title_frame, text="Text Editor", font=("Arial", 20))
    title_label.grid(column=1, row=0)

    ttk.Separator(about_window, orient="horizontal").grid(column=0, row=1, sticky="ew")

    info_frame = Frame(about_window)
    info_frame.grid(column=0, row=2, sticky="nsew")

    info_label = Label(info_frame, text="\n".join(info_content))
    info_label.grid(column=0, row=0, sticky="ew")
