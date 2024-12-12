from tkinter import *
from tkinter import ttk


def create_status_frame(app: Tk):
    app.status_frame = Frame(app, borderwidth=1)
    app.status_frame.grid(column=0, row=2, sticky="ew")

    app.status_message_label = Label(app.status_frame, text="Message", width=15)
    app.status_message_label.grid(column=0, row=0)

    ttk.Separator(app.status_frame, orient="vertical").grid(column=1, row=0, sticky="ns")

    app.status_wrap_mode_label = Label(app.status_frame, text="Wrap mode: Word", width=15)
    app.status_wrap_mode_label.grid(column=2, row=0)

    ttk.Separator(app.status_frame, orient="vertical").grid(column=3, row=0, sticky="ns")

    app.status_language_label = Label(app.status_frame, text=f"Lang: {app.language.capitalize()}", width=8)
    app.status_language_label.grid(column=4, row=0)

    ttk.Separator(app.status_frame, orient="vertical").grid(column=5, row=0, sticky="ns")
