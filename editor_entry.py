from tkinter import *


def create_editor_entry(app: Tk) -> tuple[Text, Scrollbar]:
    editor_entry = Text(
        app,
        font=app.font,
        wrap=app.wrap_mode,
        undo=True,
        insertofftime=400,
        insertontime=900
    )
    editor_entry.grid(column=0, row=0, sticky="nsew")
    editor_entry.insert("1.0", app.text)
    editor_entry.focus()
    editor_entry_scrollbar = Scrollbar(
        app,
        orient="vertical",
        jump=1
    )
    editor_entry_scrollbar.grid(column=1, row=0, sticky="ns")
    editor_entry_scrollbar.config(command=editor_entry.yview)
    editor_entry.config(yscrollcommand=editor_entry_scrollbar.set)

    return editor_entry, editor_entry_scrollbar
