from tkinter import *
from tkinter import font


class Page():
    def __init__(self, app: Tk):
        super().__init__()
        self.app = app
        self.page = Toplevel(app)
        self.page.title("Font")
        self.page.resizable(False, False)
        self.page.wm_attributes("-toolwindow", True)
        self.page.wm_attributes("-topmost", True)
        self.create_page()

    def create_page(self):
        self.font_frame = Frame(self.page)
        self.font_frame.grid(column=0, row=0, padx=5, pady=(0, 5))
        self.font_frame.grid_rowconfigure(1, weight=1)

        self.style_frame = Frame(self.page)
        self.style_frame.grid(column=1, row=0, padx=5, pady=(0, 5))
        self.style_frame.grid_rowconfigure(1, weight=1)

        self.size_frame = Frame(self.page)
        self.size_frame.grid(column=2, row=0, padx=5, pady=(0, 5))
        self.size_frame.grid_rowconfigure(1, weight=1)

        Label(self.font_frame, text=self.app.lang_dict.get("font_page.label.font")).grid(column=0, row=0)
        self.font_input = Entry(self.font_frame, border=1, relief="solid", width=20)
        self.font_input.grid(column=0, row=1)
        self.font_listbox = Listbox(self.font_frame, width=20, height=5, border=2, relief="solid")
        self.font_listbox.grid(column=0, row=2)
        self.font_listbox.insert(END, *font.families())
        self.font_listbox.bind("<Double-Button-1>", lambda event: self.update_font_input())
        self.font_listbox.bind("<Return>", lambda event: self.update_font_input())

        Label(self.style_frame, text=self.app.lang_dict.get("font_page.label.style")).grid(column=0, row=0)
        self.style_input = Entry(self.style_frame, border=1, relief="solid", width=20)
        self.style_input.grid(column=0, row=1)
        self.style_listbox = Listbox(self.style_frame, width=20, height=5, border=2, relief="solid")
        self.style_listbox.grid(column=0, row=2)
        self.style_listbox.insert(END, "Normal", "Bold", "Italic", "Underline", "Overstrike")
        self.style_listbox.bind("<Double-Button-1>", lambda event: self.update_style_input())
        self.style_listbox.bind("<Return>", lambda event: self.update_style_input())

        Label(self.size_frame, text=self.app.lang_dict.get("font_page.label.size")).grid(column=0, row=0)
        self.size_input = Entry(self.size_frame, border=1, relief="solid", width=20)
        self.size_input.grid(column=0, row=1)
        self.size_listbox = Listbox(self.size_frame, width=20, height=5, border=2, relief="solid")
        self.size_listbox.grid(column=0, row=2)
        self.size_listbox.insert(END, *[str(size) for size in range(8, 73, 2)])
        self.size_listbox.bind("<Double-Button-1>", lambda event: self.update_size_input())
        self.size_listbox.bind("<Return>", lambda event: self.update_size_input())

    def update_font_input(self):
        self.font_input.delete(0, END)
        self.font_input.insert(0, self.font_listbox.get(self.font_listbox.curselection()))

    def update_style_input(self):
        self.style_input.delete(0, END)
        self.style_input.insert(0, self.style_listbox.get(self.style_listbox.curselection()))

    def update_size_input(self):
        self.size_input.delete(0, END)
        self.size_input.insert(0, self.size_listbox.get(self.size_listbox.curselection()))
