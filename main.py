from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
WORD_FONT = ("Ariel", 60, "bold")
TITLE_FONT = ("Ariel", 40, "italic")

try:
    word_data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    word_data = pandas.read_csv("./data/french_words.csv")
finally:
    to_learn = word_data.to_dict(orient="records")


def next_card(num):
    global timer, to_learn
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    french = current_card['French']
    english = current_card['English']
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=f"{french}", fill="black")
    canvas.itemconfig(canvas_image, image=front_img)
    timer = window.after(3000, card_back, english)
    if num == 1:
        to_learn.remove(current_card)
        df = pandas.DataFrame(to_learn)
        df.to_csv("./data/words_to_learn.csv", index=False)


def card_back(english):
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=f"{english}")


# WINDOW/CANVAS
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_img)
card_title = canvas.create_text(400, 150, text="", font=TITLE_FONT)
card_word = canvas.create_text(400, 263, text="", font=WORD_FONT)
canvas.grid(column=0, row=0, columnspan=2)

timer = window.after(3000, card_back)

# BUTTONS
check_img = PhotoImage(file="./images/right.png")
check_button = Button(image=check_img, highlightthickness=0, command=lambda: next_card(1))
check_button.grid(column=1, row=1)

unknown_img = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=unknown_img, highlightthickness=0, command=lambda: next_card(0))
unknown_button.grid(column=0, row=1)

# LABELS
next_card(0)
window.mainloop()
