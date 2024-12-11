from tkinter import *
from tkinter import ttk


def create_status_frame(app: Tk) -> tuple[Frame, Label]:
    status_frame = Frame(app, height=20, borderwidth=1)
    status_frame.grid(column=0, row=2, sticky="ew")

    status_label = Label(status_frame, width=50, anchor="w")
    status_label.grid(column=0, row=0, sticky="w")

    ttk.Separator(status_frame, orient="vertical").grid(column=0, row=0, sticky="ns")

    return status_frame, status_label
