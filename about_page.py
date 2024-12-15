from tkinter import *
from tkinter import ttk


info_content = [
    "Version 1.0",
    "Luca Bertaggia"
]

links = {
    "GitHub": "https://github.com/LcBert/Text-Editor",
    "Instagram": "https://www.instagram.com/luca___bert/"
}

link_labels = []


class Page():
    def __init__(self, app: Tk):
        self.app = app
        self.page = Toplevel(app)
        self.page.transient(app)
        self.page.title(app.lang_dict.get("menubar.help.about"))
        self.page.iconbitmap("img/appicon.ico")
        self.page.resizable(False, False)
        # self.page.wm_attributes("-topmost", True)

        self.page.grid_columnconfigure(0, weight=1)

        title_frame = Frame(self.page)
        title_frame.grid(column=0, row=0, sticky="ew", padx=10)

        appicon = PhotoImage(file="img/appicon.png")
        image_label = Label(title_frame, image=appicon)
        image_label.image = appicon  # keep a reference to the image
        image_label.grid(column=0, row=0)

        title_label = Label(title_frame, text="Text Editor", font=("Arial", 20))
        title_label.grid(column=1, row=0)

        ttk.Separator(self.page, orient="horizontal").grid(column=0, row=1, sticky="ew")

        info_frame = Frame(self.page)
        info_frame.grid(column=0, row=2, sticky="ew")
        info_frame.grid_anchor("center")

        info_label = Label(info_frame, text="\n".join(info_content), font=("Arial", 12))
        info_label.grid(column=0, row=0)

        ttk.Separator(self.page, orient="horizontal").grid(column=0, row=3, sticky="ew")

        link_frame = Frame(self.page)
        link_frame.grid(column=0, row=4, sticky="ew")
        link_frame.grid_anchor("center")

        for index, link in enumerate(links):
            label = Label(
                link_frame,
                text=link,
                font=("Arial", 12, "underline"),
                fg="blue",
                cursor="hand2"
            )
            label.grid(
                column=index,
                row=0
            )
            label.bind(
                "<Button-1>",
                lambda event, link=links.get(link): self.app.open_link(link)
            )
            link_labels.append(label)
