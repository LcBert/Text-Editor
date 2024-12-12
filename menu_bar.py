from tkinter import *
from tkinter import ttk
import font_format


def __file_menu(app: Tk, menubar: Menu) -> Menu:
    app.file_menu = Menu(menubar, tearoff=0)

    app.recent_files_menu = Menu(app.file_menu, tearoff=0)
    app.recent_files_menu.add_command(label=app.lang_dict.get("menubar.file.recent.clear"), command=lambda: clear_recent_file(app))
    app.recent_files_menu.add_separator()

    app.file_menu.add_command(label=app.lang_dict.get("menubar.file.open"), accelerator="Ctrl+O", command=app.open_file)
    app.file_menu.add_command(label=app.lang_dict.get("menubar.file.save"), accelerator="Ctrl+S", command=app.save_file)
    app.file_menu.add_command(label=app.lang_dict.get("menubar.file.saveas"), accelerator="Ctrl+Shift+S", command=app.save_as_file)
    app.file_menu.add_command(label=app.lang_dict.get("menubar.file.close"), accelerator="Ctrl+Q", command=app.close_file)
    app.file_menu.add_separator()
    app.file_menu.add_command(label=app.lang_dict.get("menubar.file.explorer"), accelerator="Ctrl+E", command=app.show_in_explorer)
    app.file_menu.add_cascade(label=app.lang_dict.get("menubar.file.recent"), menu=app.recent_files_menu)
    app.file_menu.add_separator()
    app.file_menu.add_command(label=app.lang_dict.get("menubar.file.exit"), command=app.xquit)

    return app.file_menu


def __format_menu(app: Tk, menubar: Menu) -> Menu:
    app.format_menu = Menu(menubar, tearoff=0)

    app.format_wrap_submenu = Menu(app.format_menu, tearoff=0)
    app.format_wrap_submenu.add_command(label=app.lang_dict.get("menubar.format.wrap.word"), command=lambda: app.edit_wrap_content("word"))
    app.format_wrap_submenu.add_command(label=app.lang_dict.get("menubar.format.wrap.char"), command=lambda: app.edit_wrap_content("char"))
    app.format_wrap_submenu.add_command(label=app.lang_dict.get("menubar.format.wrap.none"), command=lambda: app.edit_wrap_content("none"))

    app.format_menu.add_cascade(label=app.lang_dict.get("menubar.format.wrap"), menu=app.format_wrap_submenu)
    app.format_menu.add_command(label=app.lang_dict.get("menubar.format.font"), command=lambda: font_format.Page(app))

    return app.format_menu


def __app_menu(app: Tk, menubar: Menu) -> Menu:
    app.app_menu = Menu(menubar, tearoff=0)

    app.app_language_submenu = Menu(app.app_menu, tearoff=0)
    app.app_language_submenu.add_command(label="English", command=lambda: app.change_language("en"))
    app.app_language_submenu.add_command(label="Italiano", command=lambda: app.change_language("it"))

    app.app_menu.add_cascade(label=app.lang_dict.get("menubar.app.language"), menu=app.app_language_submenu)

    return app.app_menu


def __help_menu(app: Tk, menubar: Menu) -> Menu:
    app.help_menu = Menu(menubar, tearoff=0)

    app.help_menu.add_command(label=app.lang_dict.get("menubar.help.about"), command=lambda: __help_show_about(app))

    return app.help_menu


def create_menu(app: Tk):
    app.menubar = Menu(app)
    app.config(menu=app.menubar)

    app.menubar.add_cascade(label=app.lang_dict.get("menubar.file"), menu=__file_menu(app, app.menubar))
    app.menubar.add_cascade(label=app.lang_dict.get("menubar.format"), menu=__format_menu(app, app.menubar))
    app.menubar.add_cascade(label=app.lang_dict.get("menubar.app"), menu=__app_menu(app, app.menubar))
    app.menubar.add_cascade(label=app.lang_dict.get("menubar.help"), menu=__help_menu(app, app.menubar))


def __help_show_about(app: Tk):
    info_content = [
        "Version 1.0",
        "Author: Luca Bertaggia"
    ]
    about_window = Toplevel(app)
    about_window.title(app.lang_dict.get("menubar.help.about"))
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


def refresh_recent_file_menu(app: Tk, files: list = []):
    app.recent_files_menu.delete(2, END)
    for file in files:
        app.recent_files_menu.add_command(label=file, command=lambda file=file: app.open_file(file))


def clear_recent_file(app: Tk):
    app.recent_files_menu.delete(2, END)
    app.clear_recent_file_list()
