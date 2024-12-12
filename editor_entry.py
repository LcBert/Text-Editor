from tkinter import *


def create_editor_entry(app: Tk):
    app.editor_entry = Text(
        app,
        font=app.font,
        wrap=app.wrap_mode,
        undo=True,
        insertofftime=400,
        insertontime=900
    )
    app.editor_entry.grid(column=0, row=0, sticky="nsew")
    app.editor_entry.insert("1.0", app.text)
    app.editor_entry.focus()

    app.editor_entry_scrollbar = Scrollbar(
        app,
        orient="vertical",
        jump=1
    )
    app.editor_entry_scrollbar.grid(column=1, row=0, sticky="ns")
    app.editor_entry_scrollbar.config(command=app.editor_entry.yview)
    app.editor_entry.config(yscrollcommand=app.editor_entry_scrollbar.set)
