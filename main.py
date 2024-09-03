import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import math
import random
import html

WIDTH = 1500
HEIGHT = 1500
FONT = "Helvetica", 30, "bold"
TYPE_FONT = "Helvetica", 25, "bold"
YELLOW = "#FFFFED"
LILAC = "#B1AFFF"
GREEN = "#98fb98"
DARK_GRAY = "#333333"
LIGHT_GRAY = "#EBEBE4"
LIGHT_BLUE = "#BBE9FF"
PINK = "#FF69B4"
count = 1


class TypingTest:

    def __init__(self, main_window):
        self.main_window = main_window


    def get_word_count(self):
        list_words_sample = main_window.template_text.get(1.0, "end-1c")
        words_only_sample = [word for word in list_words_sample.split() if word != " "]

        list_words = main_window.type_in_text.get(1.0, "end-1c")
        words_only = [word for word in list_words.split() if word != " "]

        similar_words = [word for word in words_only if word in words_only_sample]

        num_words = len(similar_words)

        main_window.wpm_var.set(str(num_words))

    def get_char_count(self):
        list_chars_sample = main_window.template_text.get(1.0, "end-1c")

        list_chars = main_window.type_in_text.get(1.0, "end-1c")

        similar_chars = [chars for chars in list_chars if chars in list_chars_sample]

        num_chars = len(similar_chars)

        main_window.cpm_var.set(str(num_chars))

    def start_count_down(self, count):
        main_window.type_in_text.focus()

        time_left_min = math.floor(count/60)
        time_left_sec = count % 60

        if time_left_sec < 10:
            time_left_sec = f"0{time_left_sec}"

        if count > 0:
            main_window.after(1000, self.start_count_down, count-1)
            main_window.clock_var.set(f"{time_left_min}:{time_left_sec}")
        else:
            main_window.type_in_text.config(state="disabled")
            main_window.score_var.set(f"{main_window.wpm_var.get()} WPM")
            main_window.clock_var.set("00:00")


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.typing_test = TypingTest(self)

        self.title("Typing Speed Testing App")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable=False

        self.main_style = ttk.Style()
        self.main_style.configure("main_style.TFrame", theme="cyborg")

        self.main_frame = ttk.Frame(self, style="main_style.TFrame")
        self.main_frame.columnconfigure(0, weight=2)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.pack(fill="both", expand=True)

        self.top_frame = ttk.Frame(self.main_frame, width=WIDTH, height=700, style="main_style.TFrame")
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(1, weight=1)
        self.top_frame.grid(row=0, column=0, ipady=5, padx=2, pady=5)

        self.bottom_frame = ttk.Frame(self.main_frame, width=WIDTH, height=800)
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(1, weight=1)
        self.bottom_frame.grid(row=1, column=0, ipady=5, padx=2, pady=5)

        self.top_widgets()
        self.typing_widgets()
        self.restart()

    def top_widgets(self):

        title = ttk.Label(self.top_frame,
                          text="YOUR TYPING SPEED",
                          font=FONT,
                          background=LIGHT_BLUE,
                          foreground=LILAC)
        title.grid(row=0, column=1, pady=5, padx=50)

        score = ttk.Label(self.top_frame,
                          text="Score:",
                          font=FONT,
                          justify="left",
                          background=LIGHT_BLUE,
                          foreground=LILAC)
        score.grid(row=1, column=0, pady=5, padx=50)

        self.score_var = tk.StringVar()
        score_entry = ttk.Entry(self.top_frame,
                                textvariable=self.score_var,
                                font=FONT,
                                justify="center",
                                foreground=PINK,
                                width=8)
        score_entry.grid(row=1, column=1, pady=5, padx=50)

        words_per_min = ttk.Label(self.top_frame,
                                  text="WPM:",
                                  font=FONT,
                                  justify="center",
                                  background=LIGHT_BLUE,
                                  foreground=LILAC)
        words_per_min.grid(row=2, column=0, pady=5, padx=50)

        self.wpm_var = tk.StringVar()
        wpm_entry = ttk.Entry(self.top_frame,
                              textvariable=self.wpm_var,
                              font=FONT,
                              justify="center",
                              foreground=PINK,
                              width=8)
        wpm_entry.grid(row=3, column=0, pady=5, padx=50)

        characters_per_min = ttk.Label(self.top_frame,
                                       text="CPM:",
                                       font=FONT,
                                       justify="center",
                                       background=LIGHT_BLUE,
                                       foreground=LILAC)
        characters_per_min.grid(row=2, column=1, pady=5, padx=50)

        self.cpm_var = tk.StringVar()
        cpm_entry = ttk.Entry(self.top_frame,
                              textvariable=self.cpm_var,
                              font=FONT,
                              justify="center",
                              foreground=PINK,
                              width=8)
        cpm_entry.grid(row=3, column=1, pady=5, padx=50)

        timer = ttk.Label(self.top_frame, text="Timer",
                          background=LIGHT_BLUE,
                          foreground=LILAC,
                          font=FONT)
        timer.grid(row=0, column=2, padx=50, pady=5)

        formatted_clock_img = Image.open("resized_hourglass.jpg")

        self.clock_img = ImageTk.PhotoImage(formatted_clock_img)

        clock_label = ttk.Label(self.top_frame, image=self.clock_img, font=TYPE_FONT, justify="center")

        clock_label.grid(row=1, column=2)

        self.clock_var = tk.StringVar()
        self.clock_var.set("00:00")
        self.clock_min = ttk.Entry(self.top_frame,
                                   textvariable=self.clock_var,
                                   background=DARK_GRAY,
                                   foreground=PINK,
                                   font=TYPE_FONT,
                                   width=9,
                                   justify="center")
        self.clock_min.grid(row=2, column=2)

    def typing_widgets(self):

        instructions_label = ttk.Label(self.bottom_frame,
                                       text="Reproduce the text shown in the empty text area below!",
                                       foreground=PINK,
                                       background=LIGHT_BLUE,
                                       font=("Times New Romans", 25, "bold"),
                                       justify="center",
                                       width=69)
        instructions_label.grid(row=0, column=0, sticky="nsew", ipadx=10, ipady=10, padx=50)

        self.template_text = ScrolledText(self.bottom_frame,
                                          font=TYPE_FONT,
                                          wrap="word",
                                          width=69,
                                          height=5)
        self.template_text.config(background=YELLOW, foreground=LILAC)
        self.template_text.insert(1.0, self.sample_text())
        self.template_text.config(state="disabled")
        self.template_text.grid(row=1,
                                column=0,
                                sticky="nsew",
                                ipadx=60,
                                ipady=20,
                                padx=50)

        self.type_in_text = ScrolledText(self.bottom_frame,
                                         font=("Helvetica", 25, "bold"),
                                         wrap="word",
                                         width=69,
                                         height=3)
        self.type_in_text.config(background=LIGHT_GRAY, foreground=PINK)

        self.type_in_text.grid(row=2, column=0, sticky="nsew", padx=50)
        self.type_in_text.bind("<Key>", lambda event: self.typing_test.get_char_count())
        self.type_in_text.bind("<Key>", lambda event: self.typing_test.get_word_count(), add="+")
        self.type_in_text.bind("<FocusIn>",
                               lambda event, count=count*60:
                               self.typing_test.start_count_down(count),
                               add="+")

        self.restart_btn_style = ttk.Style()
        self.restart_btn_style.configure("restart.TButton", font=TYPE_FONT, foreground=PINK, background=LIGHT_BLUE)
        restart_button = ttk.Button(self.bottom_frame, text="RESTART", command=self.restart, style="restart.TButton")
        restart_button.grid(row=3, column=0, pady=10)

    def sample_text(self):
        with open("template.txt", "r") as sample_file:
            sample_text = sample_file.readlines()

        paragraphs = [line for line in sample_text if line.strip() != '']

        chosen_paragraph = random.randint(0, len(paragraphs) - 1)

        the_paragraph = html.unescape(paragraphs[chosen_paragraph])

        return the_paragraph

    def restart(self):
        self.type_in_text.config(state="normal")
        self.type_in_text.delete(1.0, tk.END)
        self.clock_var.set("00:00")
        self.cpm_var.set("")
        self.wpm_var.set("")
        self.score_var.set("")


if "__main__" == __name__:
    main_window = MainWindow()

    main_window.mainloop()

