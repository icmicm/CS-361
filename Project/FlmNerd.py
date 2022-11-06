import random
import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
from random import *
import json
import unidecode
import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:5557")

with open("actors.json", "r") as f:
    actor_start = json.load(f)

bg_colour = "#3d6466"

player = "Ian"
novice_plays = 0
novice_wins = 0
intermediate_plays = 0
intermediate_wins = 0
master_plays = 0
master_wins = 0
total_plays = 0

titles = []
actors = []

def get_movies(person, difficulty):
    socket.send_pyobj(["actor", person])
    movies = socket.recv_pyobj()
    for movie in movies:
        if movie in titles:
            movies.remove(movie)
            continue
        else:
            titles.append(movies[0])
            return movies[0]


def get_actor(movie, difficulty):
    socket.send_pyobj(["movie", movie])
    persons = socket.recv_pyobj()
    for person in persons:
        if person in actors:
            persons.remove(person)
            continue
        else:
            actors.append(persons[0])
            return persons[0]

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def difficulty_clicked(value):
    if (value == "Novice" and novice_plays == 0) or (value == "Intermediate" and intermediate_plays == 0) or (
            value == "Master" and master_plays == 0):
        tk.Button(frame3, text="START!", font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black",
                  command=lambda: load_frame4(frame3, value)).grid(row=6, column=1, pady=20)
    else:
        tk.Button(frame3, text="START!", font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black",
                  command=lambda: load_frame5(frame3, value, 1, None)).grid(row=6, column=1, pady=20)


def answer_clicked(value, correct, difficulty, round):
    if value == correct and round == 6:
        tk.Button(frame5, text="SUBMIT", font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black",
                  command=lambda: load_frame6(frame5, difficulty, "WIN")).grid(row=8, column=1, pady=20)
    elif value == correct and round < 6:
        tk.Button(frame5, text="SUBMIT", font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black",
                  command=lambda: load_frame5(frame5, difficulty, round + 1, correct)).grid(row=8, column=1, pady=20)
    else:
        tk.Button(frame5, text="SUBMIT", font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black",
                  command=lambda: load_frame6(frame5, difficulty, "LOSE")).grid(row=8, column=1, pady=20)


def load_frame1():

    clear_widgets(frame2)
    frame1.grid(row=0, column=0, sticky="nesw")
    frame1.tkraise()
    frame1.pack_propagate(False)

    # frame1 widgets
    title_img = ImageTk.PhotoImage(file="images/FILM_NERD.png")
    title_widget = tk.Label(frame1, image=title_img, bg=bg_colour)
    title_widget.image = title_img
    title_widget.pack(pady=100)

    tk.Label(frame1, text="Enter Player Name:", bg=bg_colour, fg="white", font=("TkMenuFont", 14)).pack()

    name = tk.Entry(frame1, width=35, font="bold", bg="white", fg="black", borderwidth=5)
    name.pack()

    if novice_plays == 0:
        tk.Button(frame1, text="ENTER", font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black",
                  command=lambda: load_frame2(frame1, name.get())).pack(pady=20)
    else:
        tk.Button(frame1, text="ENTER", font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
                  activebackground="#badee2", activeforeground="black",
                  command=lambda: load_frame3(frame1)).pack(pady=20)


def load_frame2(last_frame, name):
    clear_widgets(last_frame)
    frame2.tkraise()
    frame2.grid(row=0, column=0, sticky="nesw")
    frame2.pack_propagate(False)

    title_img = ImageTk.PhotoImage(file="images/FILM_NERD.png")
    title_widget = tk.Label(frame2, image=title_img, bg=bg_colour)
    title_widget.image = title_img
    title_widget.pack(pady=100)

    tk.Label(frame2, text="WELCOME TO FILM NERD " + name.upper() + "!", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 20)).pack()
    tk.Label(frame2, text="Beat the game in Novice mode to unlock the next difficulty setting", bg=bg_colour,
             fg="white", font=("TkMenuFont", 14)).pack()

    tk.Button(frame2, text="GOT IT!", font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black",
              command=lambda: load_frame3(frame2)).pack(pady=20)


def load_frame3(last_frame):
    global titles
    global actors
    titles = []
    actors = []
    clear_widgets(last_frame)
    frame3.tkraise()
    frame3.grid(row=0, column=0, sticky="nesw")
    frame3.columnconfigure(0, weight=1)
    frame3.columnconfigure(1, weight=1)
    frame3.columnconfigure(2, weight=1)
    frame3.pack_propagate(False)

    tk.Label(frame3, text=player, bg=bg_colour, fg="red",
             font=("TkHeadingFont", 20)).grid(row=0, column=0, sticky=tk.W)

    title_img = ImageTk.PhotoImage(file="images/FILM_NERD.png")
    title_widget = tk.Label(frame3, image=title_img, bg=bg_colour)
    title_widget.image = title_img
    title_widget.grid(row=1, column=1, pady=50)

    tk.Label(frame3, text="Select your difficulty", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 20)).grid(row=2, column=1, pady=30)

    difficulty = tk.StringVar()
    difficulty.set(None)

    if novice_wins == 0:
        rb2_state = "disabled"
    else:
        rb2_state = "normal"

    if intermediate_wins == 0:
        rb3_state = "disabled"
    else:
        rb3_state = "normal"
    tk.Radiobutton(frame3, selectcolor=bg_colour, text="Novice", font=("TkMenuFont", 20), bg=bg_colour, fg="white",
                   variable=difficulty, value="Novice", command=lambda: difficulty_clicked(difficulty.get())).grid(
        row=3, column=1,
        sticky=tk.W,
        padx=400)
    tk.Radiobutton(frame3, selectcolor=bg_colour, text="Intermediate", font=("TkMenuFont", 20), bg=bg_colour,
                   fg="white", variable=difficulty, value="Intermediate", state=rb2_state,
                   command=lambda: difficulty_clicked(difficulty.get())).grid(row=4, column=1, sticky=tk.W, padx=400)
    tk.Radiobutton(frame3, selectcolor=bg_colour, text="Master", font=("TkMenuFont", 20), bg=bg_colour, fg="white",
                   variable=difficulty, value="Master", state=rb3_state,
                   command=lambda: difficulty_clicked(difficulty.get())).grid(row=5, column=1,
                                                                              sticky=tk.W,
                                                                              padx=400)

    tk.Button(frame3, text="RULES", font=("TkMenuFont", 10), bg="red", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black",
              command=lambda: load_frame4(frame3, "Novice")).grid(row=3, column=1, sticky=tk.E, padx=300)

    tk.Button(frame3, text="RULES", font=("TkMenuFont", 10), bg="red", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black", state=rb2_state,
              command=lambda: load_frame4(frame3, "Intermediate")).grid(row=4, column=1, sticky=tk.E, padx=300)

    tk.Button(frame3, text="RULES", font=("TkMenuFont", 10), bg="red", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black", state=rb3_state,
              command=lambda: load_frame4(frame3, "Master")).grid(row=5, column=1, sticky=tk.E, padx=300)


def load_frame4(last_frame, difficulty):
    clear_widgets(last_frame)
    frame4.tkraise()
    frame4.grid(row=0, column=0, sticky="nesw")
    frame4.columnconfigure(0, weight=1)
    frame4.columnconfigure(1, weight=1)
    frame4.columnconfigure(2, weight=1)
    frame4.pack_propagate(False)

    tk.Label(frame4, text=player, bg=bg_colour, fg="red",
             font=("TkHeadingFont", 20)).grid(row=0, column=0, sticky=tk.W)

    tk.Label(frame4, text="GAMEPLAY", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 35)).grid(row=1, column=1, pady=30)

    if difficulty == "Novice":
        msg = "You will be presented with an Actress/Actor, and the title of a movie they were in.\n" \
              "You will also be presented with a list of potential co-stars,\n" \
              "you will have 40 seconds to choose the correct co-star to continue to the next round.\n\n" \
              "The next round will be the same,\n" \
              "but the Actress/Actor will be the correct answer from the previous round!\n" \
              "If you finish all six rounds, you win.\n\n" \
              "Good Luck!"
    elif difficulty == "Intermediate":
        msg = "The game play in this mode is identical to the \"Novice\" mode.\n" \
              "However, in this mode don't expect every movie to be a blockbuster hit!\n" \
              "And you will only have 30 seconds per round.\n\n" \
              "Good Luck!"
    else:
        msg = "This is the hardest game mode!\n" \
              "Clearly you are looking for a challenge.\n\n" \
              "The rules of the game have not changed,\n" \
              "however, in this mode we  will not give you the main character.\n\n" \
              "Good Luck!"

    tk.Label(frame4, text=msg, bg=bg_colour, fg="white",
             font=("TkHeadingFont", 20)).grid(row=2, column=0, columnspan=3, pady=30)

    tk.Button(frame4, text="PLAY", font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black",
              command=lambda: load_frame5(frame4, difficulty, 1, None)).grid(row=3, column=1, pady=20)

    tk.Button(frame4, text="Choose Different Level", font=("TkHeadingFont", 14), bg="red", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black",
              command=lambda: load_frame3(frame4)).grid(row=4, column=1, pady=10)


def load_frame5(last_frame, difficulty, round, person):
    clear_widgets(last_frame)
    frame5.tkraise()
    frame5.grid(row=0, column=0, sticky="nesw")
    frame5.columnconfigure(0, weight=1)
    frame5.columnconfigure(1, weight=1)
    frame5.columnconfigure(2, weight=1)
    frame5.pack_propagate(False)

    def countdown(seconds):
        sec = seconds - 1
        timer.config(text=str(sec))
        if sec <= 10:
            timer.config(fg="red")
        if sec == 0:
            load_frame6(frame5, difficulty, "LOSE")
            return
        timer.after(1000, lambda: countdown(sec))

    if round == 1:
        person = unidecode.unidecode(actor_start[randint(0, 99)]["Name"])
        socket.send_pyobj([person])
        start_data = socket.recv_pyobj()
        title = start_data[0]
        socket.send_pyobj(["movie", title])
        correct_answer = socket.recv_pyobj()
        correct_answer.remove(person)
        correct_answer = correct_answer[0]
        titles.append(title)
        actors.append(correct_answer)
        actors.append(person)
    else:
        title = get_movies(person, difficulty)
        correct_answer = get_actor(title, difficulty)

    actor_answers = [correct_answer]
    while len(actor_answers) <= 3:
        actor = unidecode.unidecode(actor_start[randint(0, 99)]["Name"])
        if actor not in actor_answers and actor not in actors:
            actor_answers.append(actor)
    shuffle(actor_answers)

    answer = tk.StringVar()
    answer.set(None)

    tk.Label(frame5, text=player, bg=bg_colour, fg="red",
             font=("TkHeadingFont", 20)).grid(row=0, column=0, sticky=tk.W)

    tk.Label(frame5, text="ROUND " + str(round) + " OF 6", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 35)).grid(row=1, column=1, pady=30)

    timer = tk.Label(frame5, text="45", bg=bg_colour, fg="white", font=("TkHeadingFont", 40))
    timer.grid(row=2, column=0, columnspan=3, pady=5)
    if difficulty == "Novice":
        countdown(40)
    elif difficulty == "Intermediate":
        countdown(30)
    else:
        countdown(20)

    tk.Label(frame5, text=person + " was in " + title + " with:", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 20)).grid(row=3, column=0, columnspan=3, pady=30)

    x = 4
    for text in actor_answers:
        tk.Radiobutton(frame5, selectcolor=bg_colour, text=text, font=("TkMenuFont", 20), bg=bg_colour,
                       fg="white", variable=answer, value=text,
                       command=lambda: answer_clicked(answer.get(), correct_answer, difficulty, round)).grid(row=x,
                                                                                                             column=1,
                                                                                                             sticky=tk.W,
                                                                                                             padx=400)
        x += 1


def load_frame6(last_frame, difficulty, outcome):
    clear_widgets(last_frame)
    frame6.tkraise()
    frame6.grid(row=0, column=0, sticky="nesw")
    frame6.columnconfigure(0, weight=1)
    frame6.columnconfigure(1, weight=1)
    frame6.columnconfigure(2, weight=1)
    frame6.pack_propagate(False)

    # make a db
    """
    total_plays += 1

    if difficulty == "Novice":
        novice_plays += 1
        if outcome == "WIN":
            novice_wins += 1

    if difficulty == "Intermediate":
        intermediate_play += 1
        if outcome == "WIN":
            intermediate_wins += 1

    if difficulty == "Master":
        master_plays += 1
        if outcome == "WIN":
            master_wins += 1
    """

    tk.Label(frame6, text=player, bg=bg_colour, fg="red",
             font=("TkHeadingFont", 20)).grid(row=0, column=0, sticky=tk.W)

    tk.Label(frame6, text="YOU " + outcome + ", " + player.upper() + "!", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 35)).grid(row=1, column=1, pady=30)

    tk.Label(frame6, text="Novice games played: " + str(novice_plays), bg=bg_colour, fg="white",
             font=("TkMenuFont", 12)).grid(row=2, column=0, pady=10)

    tk.Label(frame6, text="Novice games won: " + str(novice_wins), bg=bg_colour, fg="white",
             font=("TkMenuFont", 12)).grid(row=3, column=0, pady=10)

    tk.Label(frame6, text="Novice games lost: " + str(novice_plays - novice_wins), bg=bg_colour, fg="white",
             font=("TkMenuFont", 12)).grid(row=4, column=0, pady=10)

    tk.Label(frame6, text="Intermediate games played: " + str(intermediate_plays), bg=bg_colour, fg="white",
             font=("TkMenuFont", 12)).grid(row=2, column=1, pady=10)

    tk.Label(frame6, text="Intermediate games won: " + str(intermediate_wins), bg=bg_colour, fg="white",
             font=("TkMenuFont", 12)).grid(row=3, column=1, pady=10)

    tk.Label(frame6, text="Intermediate games lost: " + str(intermediate_plays - intermediate_wins), bg=bg_colour,
             fg="white",
             font=("TkMenuFont", 12)).grid(row=4, column=1, pady=10)

    tk.Label(frame6, text="Master games played: " + str(master_plays), bg=bg_colour, fg="white",
             font=("TkMenuFont", 12)).grid(row=2, column=2, pady=10)

    tk.Label(frame6, text="Master games won: " + str(master_wins), bg=bg_colour, fg="white",
             font=("TkMenuFont", 12)).grid(row=3, column=2, pady=10)

    tk.Label(frame6, text="Master games lost: " + str(master_plays - master_wins), bg=bg_colour,
             fg="white",
             font=("TkMenuFont", 12)).grid(row=4, column=2, pady=10)

    tk.Button(frame6, text="NEW GAME", font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black",
              command=lambda: load_frame3(frame6)).grid(row=5, column=1, pady=50)

    tk.Button(frame6, text="EXIT", font=("TkHeadingFont", 14), bg="red", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black", command=root.destroy).grid(row=6, column=1, pady=0)


# initialize the app
root = tk.Tk()
root.title("Film Nerd")
root.iconbitmap("images/tripod.ico")
root.eval("tk::PlaceWindow . center")

# place the window
# x = root.winfo_screenwidth() // 2
# y = int(root.winfo_screenheight() * 0.1)
# root.geometry("1000x600+" + str(x) + "+" + str(y))

# create frame1
frame1 = tk.Frame(root, width=1000, height=600, bg=bg_colour)
frame2 = tk.Frame(root, width=1000, height=600, bg=bg_colour)
frame3 = tk.Frame(root, width=1000, height=600, bg=bg_colour)
frame4 = tk.Frame(root, width=1000, height=600, bg=bg_colour)
frame5 = tk.Frame(root, width=1000, height=600, bg=bg_colour)
frame6 = tk.Frame(root, width=1000, height=600, bg=bg_colour)

# frame2.grid(row=0, column=0)


load_frame1()
# run the app
root.mainloop()

"""
def get_movies(actor, difficulty):
    movies = []
    for movie in data:
        if difficulty is "Intermediate":
            if float(movie[2]) >= 8.0:
                continue
        elif difficulty is "Master":
            if int(movie[1]) > 1960:
                continue
        people = movie[3]
        if difficulty is "Intermediate":
            people = people[2:3]
        for person in people:
            if person is actor:
                movies
"""
