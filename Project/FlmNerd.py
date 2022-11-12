import random
import tkinter as tk
from PIL import ImageTk
from random import *
import json
import unidecode
import zmq

# connect to the IMDB scraper microservice
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:5557")

# read in list of top actors/actresses
with open("actors.json", "r") as f:
    actor_start_normal = json.load(f)

# read in a list of silver screen actors and actresses
with open("silver_screen.json", "r") as f:
    actor_start_oldies = json.load(f)

# background colour for all app pages
bg_colour = "#3d6466"

# session data (scores) for the player
player = ""
novice_plays = 0
novice_wins = 0
intermediate_plays = 0
intermediate_wins = 1
master_plays = 0
master_wins = 0
total_plays = 0

# list of actors and movie titles initialized as global variables for later use
titles = []
actors = []


# sends an actor name to the microservice and receives a list of movies that actor has been in
# the lis of movies is then formatted to suit the difficultly setting of the game.
def get_movies(person, difficulty):
    socket.send_pyobj(["actor", person])
    movies = socket.recv_pyobj()
    for movie in movies:
        if movie in titles:
            movies.remove(movie)
            continue
        # if difficulty is set to intermediate, do not return the most obvious answer
        elif difficulty == "Intermediate":
            titles.append(movies[2])
            return movies[2]
        else:
            titles.append(movies[0])
            return movies[0]


# sends a movie title to the microservice and receives a list of actors that were in that movie
def get_actor(movie, difficulty):
    socket.send_pyobj(["movie", movie])
    persons = socket.recv_pyobj()
    for person in persons:
        if person in actors:
            persons.remove(person)
            continue
        # if difficulty is set to intermediate, do not return the most obvious answer
        elif difficulty == "Intermediate":
            actors.append((persons[1]))
            return persons[1]
        else:
            actors.append(persons[0])
            return persons[0]


# clears all items on in the current app window
def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# places the title image in the desired frame
def title(this_frame, placement):
    title_img = ImageTk.PhotoImage(file="images/FILM_NERD.png")
    title_widget = tk.Label(this_frame, image=title_img, bg=bg_colour)
    title_widget.image = title_img
    if placement == "pack":
        title_widget.pack(pady=100)
    elif placement == "grid":
        title_widget.grid(row=1, column=1, pady=50)


# displays the player name in the window
def show_name(current_frame, name):
    tk.Label(current_frame, text=name, bg=bg_colour, fg="red",
             font=("TkHeadingFont", 20)).grid(row=0, column=0, sticky=tk.W)


# create buttons that use the grid method
def grid_button(text, row, current_frame, next_frame, colour):
    tk.Button(current_frame, text=text, font=("TkHeadingFont", 14), bg=colour, fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black",
              command=next_frame).grid(row=row, column=1, pady=20)


# create buttons that use the pack method
def pack_button(text, current_frame, next_frame):
    tk.Button(current_frame, text=text, font=("TkHeadingFont", 14), bg="green", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black",
              command=next_frame).pack(pady=20)


# buttons to go to the rules pages
def rules_buttons(text, current_frame, state, next_frame, row):
    tk.Button(current_frame, text=text, font=("TkMenuFont", 10), bg="red", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black", state=state,
              command=next_frame).grid(row=row, column=1, sticky=tk.E, padx=300)


# radio buttons to select the gameplay difficulty
def difficulty_radio_button(text, current_frame, difficulty, state, row):
    tk.Radiobutton(current_frame, selectcolor=bg_colour, text=text, font=("TkMenuFont", 20), bg=bg_colour, fg="white",
                   variable=difficulty, value=text, state=state,
                   command=lambda: difficulty_clicked(difficulty.get())).grid(row=row, column=1, sticky=tk.W, padx=400)


# set up individual frames
def frame_setup(new_frame, old_frame):
    clear_widgets(old_frame)
    new_frame.grid(row=0, column=0, sticky="nesw")
    new_frame.tkraise()
    new_frame.pack_propagate(False)

    grid_frames = [frame3, frame4, frame5, frame6]
    if new_frame in grid_frames:
        new_frame.columnconfigure(0, weight=1)
        new_frame.columnconfigure(1, weight=1)
        new_frame.columnconfigure(2, weight=1)


# defines the functionality of clicking the stat button on the difficulty selection page
def difficulty_clicked(value):
    # If the player has NOT played this difficulty before, force them to the rules page
    if (value == "Novice" and novice_plays == 0) or (value == "Intermediate" and intermediate_plays == 0) or (
            value == "Master" and master_plays == 0):
        grid_button("START!", 6, frame3, lambda: load_frame4(frame3, value), "green")
    # if the player has played this difficulty before, let them start the game
    else:
        grid_button("START!", 6, frame3, lambda: load_frame5(frame3, value, 1, None), "green")


# defines the functionality of the SUBMIT button during the game.
def answer_clicked(value, correct, difficulty, round_num):
    # player answers the last question correctly, and wins the game
    if value == correct and round_num == 2:
        grid_button("SUBMIT", 8, frame5, lambda: load_frame6(frame5, difficulty, "WIN"), "green")
    # player answers a question correctly and moves on to the next round
    elif value == correct and round_num < 2:
        grid_button("SUBMIT", 8, frame5, lambda: load_frame5(frame5, difficulty, round_num + 1, correct), "green")
    # player answers incorrectly and loses the game
    else:
        grid_button("SUBMIT", 8, frame5, lambda: load_frame6(frame5, difficulty, "LOSE"), "green")


def load_frame1():
    frame_setup(frame1, frame2)
    title(frame1, "pack")

    # name enter text box
    tk.Label(frame1, text="Enter Player Name:", bg=bg_colour, fg="white", font=("TkMenuFont", 14)).pack()
    name = tk.Entry(frame1, width=35, font="bold", bg="white", fg="black", borderwidth=5)
    name.pack()

    # go to welcome screen if first play through
    if novice_plays == 0:
        pack_button("ENTER", frame1, lambda: load_frame2(frame1, name.get()))
    # continue to the game if not first time playing
    else:
        pack_button("ENTER", frame1, lambda: load_frame3(frame1))


def load_frame2(last_frame, name):
    global player
    player = name
    frame_setup(frame2, last_frame)
    title(frame2, "pack")

    # welcome message
    tk.Label(frame2, text="WELCOME TO FILM NERD " + player.upper() + "!", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 20)).pack()
    tk.Label(frame2, text="Beat the game in Novice mode to unlock the next difficulty setting", bg=bg_colour,
             fg="white", font=("TkMenuFont", 14)).pack()

    # acknowledgment button
    pack_button("GOT IT!", frame2, lambda: load_frame3(frame2))


def load_frame3(last_frame):
    # reset the list of actors and titles for each play through
    global titles
    global actors
    titles = []
    actors = []

    # set up the page elements
    frame_setup(frame3, last_frame)
    show_name(frame3, player)
    title(frame3, "grid")
    tk.Label(frame3, text="Select your difficulty", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 20)).grid(row=2, column=1, pady=30)

    # initialize the difficulty setting
    difficulty = tk.StringVar()
    difficulty.set(None)

    # enable or disable the radio buttons depending on if the user has beat the previous level
    if novice_wins == 0:
        rb2_state = "disabled"
    else:
        rb2_state = "normal"
    if intermediate_wins == 0:
        rb3_state = "disabled"
    else:
        rb3_state = "normal"

    # create the radio buttons for the difficulty selection
    difficulty_radio_button("Novice", frame3, difficulty, "normal", 3)
    difficulty_radio_button("Intermediate", frame3, difficulty, rb2_state, 4)
    difficulty_radio_button("Master", frame3, difficulty, rb3_state, 5)

    # create the buttons that link to the specific rules pages for each difficulty
    rules_buttons("RULES", frame3, "normal", lambda: load_frame4(frame3, "Novice"), 3)
    rules_buttons("RULES", frame3, rb2_state, lambda: load_frame4(frame3, "Intermediate"), 4)
    rules_buttons("RULES", frame3, rb3_state, lambda: load_frame4(frame3, "Master"), 5)


def load_frame4(last_frame, difficulty):
    # set up the page elements
    frame_setup(frame4, last_frame)
    show_name(frame4, player)

    # messages to the player on the different gameplay for each difficulty setting
    tk.Label(frame4, text="GAMEPLAY", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 35)).grid(row=1, column=1, pady=30)
    if difficulty == "Novice":
        msg = "You will be presented with an Actress/Actor, and the title of a movie they were in.\n" \
              "You will also be presented with a list of potential co-stars,\n" \
              "you will have 30 seconds to choose the correct co-star to continue to the next round.\n\n" \
              "The next round will be the same,\n" \
              "but the Actress/Actor will be the correct answer from the previous round!\n" \
              "If you finish all six rounds, you win.\n\n" \
              "Good Luck!"
        grid_button("PLAY", 3, frame4, lambda: load_frame5(frame4, difficulty, 1, None), "green")
    elif difficulty == "Intermediate":
        msg = "The game play in this mode is identical to the \"Novice\" mode.\n" \
              "However, in this mode don't expect every movie to be a blockbuster hit,\n" \
              "we dont plan on giving you the main character,\n" \
              "and you will only have 15 seconds per round.\n\n" \
              "Good Luck!"
        grid_button("PLAY", 3, frame4, lambda: load_frame5(frame4, difficulty, 1, None), "green")
    else:
        msg = "This is the hardest game mode!\n" \
              "Clearly you are looking for a challenge.\n\n" \
              "In this mode you still only have 15 seconds.\n" \
              "and we will focus on the oldies.\n\n" \
              "Good Luck!"
        grid_button("PLAY", 3, frame4, lambda: load_frame5(frame4, difficulty, 1, None), "green")

    # display one of the above messages
    tk.Label(frame4, text=msg, bg=bg_colour, fg="white",
             font=("TkHeadingFont", 20)).grid(row=2, column=0, columnspan=3, pady=30)

    # display the button to go back and choose a different setting
    grid_button("Choose Different Level", 4, frame4, lambda: load_frame3(frame4), "red")


# use static data to initialize the first round
def round_one(difficulty):
    if difficulty == "Master":
        person = unidecode.unidecode(actor_start_oldies[randint(0, 100)]["Name"])
    else:
        person = unidecode.unidecode(actor_start_normal[randint(0, 239)]["Name"])
    socket.send_pyobj([person])
    start_data = socket.recv_pyobj()
    film = start_data[0]
    socket.send_pyobj(["movie", film])
    correct_answer = socket.recv_pyobj()
    if person in correct_answer:
        correct_answer.remove(person)
    correct_answer = correct_answer[0]
    titles.append(film)
    actors.append(correct_answer)
    actors.append(person)
    return [person, film, correct_answer]


def load_frame5(last_frame, difficulty, level, person):
    # set up page element
    frame_setup(frame5, last_frame)
    show_name(frame5, player)
    tk.Label(frame5, text="ROUND " + str(level) + " OF 6", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 35)).grid(row=1, column=1, pady=30)

    # countdown timer for the round
    def countdown(seconds):
        sec = seconds - 1
        timer.config(text=str(sec))
        if sec <= 10:
            timer.config(fg="red")
        if sec == 0:
            load_frame6(frame5, difficulty, "LOSE")
            return
        timer.after(1000, lambda: countdown(sec))

    # initialize the game with static data for the first round
    if level == 1:
        start = round_one(difficulty)
        person = start[0]
        film = start[1]
        correct_answer = start[2]
    # use previous round information for follow-on rounds
    else:
        film = get_movies(person, difficulty)
        correct_answer = get_actor(film, difficulty)
    print(titles)
    print(actors)

    # fill the wrong answers from a static list of actors
    actor_answers = [correct_answer]
    while len(actor_answers) <= 3:
        if difficulty == "Master":
            actor = unidecode.unidecode(actor_start_oldies[randint(0, 100)]["Name"])
        else:
            actor = unidecode.unidecode(actor_start_normal[randint(0, 239)]["Name"])
        if actor not in actor_answers and actor not in actors:
            actor_answers.append(actor)
    shuffle(actor_answers)

    # start the round timer
    timer = tk.Label(frame5, text="45", bg=bg_colour, fg="white", font=("TkHeadingFont", 40))
    timer.grid(row=2, column=0, columnspan=3, pady=5)
    if difficulty == "Novice":
        countdown(30)
    elif difficulty == "Intermediate":
        countdown(15)
    else:
        countdown(15)

    # present the question to the player
    tk.Label(frame5, text=person + " was in \"" + film + "\" with:", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 20)).grid(row=3, column=0, columnspan=3, pady=30)

    # initialize the answer variable
    answer = tk.StringVar()
    answer.set(None)

    # place the possible answers as radio buttons on the page
    x = 3
    for text in actor_answers:
        x += 1
        tk.Radiobutton(frame5, selectcolor=bg_colour, text=text, font=("TkMenuFont", 20), bg=bg_colour,
                       fg="white", variable=answer, value=text,
                       command=lambda: answer_clicked(answer.get(), correct_answer, difficulty, level)) \
            .grid(row=x, column=1, sticky=tk.W, padx=400)


# create player stat widgets
def player_stats(text, row, column):
    tk.Label(frame6, text=text, bg=bg_colour, fg="white", font=("TkMenuFont", 12)).grid(row=row, column=column, pady=10)


def load_frame6(last_frame, difficulty, outcome):
    frame_setup(frame6, last_frame)
    show_name(frame6, player)

    # access global variables
    global novice_plays
    global novice_wins
    global intermediate_plays
    global intermediate_wins
    global master_plays
    global master_wins
    global total_plays
    global total_plays

    # update player stats
    total_plays += 1
    if difficulty == "Novice":
        novice_plays += 1
        if outcome == "WIN":
            novice_wins += 1
    if difficulty == "Intermediate":
        intermediate_plays += 1
        if outcome == "WIN":
            intermediate_wins += 1
    if difficulty == "Master":
        master_plays += 1
        if outcome == "WIN":
            master_wins += 1

    # Win / Lose message
    tk.Label(frame6, text="YOU " + outcome + ", " + player.upper() + "!", bg=bg_colour, fg="white",
             font=("TkHeadingFont", 35)).grid(row=1, column=1, pady=30)

    # display player stats
    player_stats("Novice games played: " + str(novice_plays), 2, 0)
    player_stats("Novice games won: " + str(novice_wins), 3, 0)
    player_stats("Novice games lost: " + str(novice_plays - novice_wins), 4, 0)
    player_stats("Intermediate games played: " + str(intermediate_plays), 2, 1)
    player_stats("Intermediate games won: " + str(intermediate_wins), 3, 1)
    player_stats("Intermediate games lost: " + str(intermediate_plays - intermediate_wins), 4, 1)
    player_stats("Master games played: " + str(master_plays), 2, 2)
    player_stats("Master games won: " + str(master_wins), 3, 2)
    player_stats("Master games lost: " + str(master_plays - master_wins), 4, 2)

    grid_button("NEW GAME", 5, frame6, lambda: load_frame3(frame6), "green")
    grid_button("EXIT", 6, frame6, root.destroy, "red")


# initialize the app
root = tk.Tk()
root.title("Film Nerd")
root.iconbitmap("images/tripod.ico")
root.eval("tk::PlaceWindow . center")

# create the frames
frame1 = tk.Frame(root, width=1000, height=600, bg=bg_colour)
frame2 = tk.Frame(root, width=1000, height=600, bg=bg_colour)
frame3 = tk.Frame(root, width=1000, height=600, bg=bg_colour)
frame4 = tk.Frame(root, width=1000, height=600, bg=bg_colour)
frame5 = tk.Frame(root, width=1000, height=600, bg=bg_colour)
frame6 = tk.Frame(root, width=1000, height=600, bg=bg_colour)

# run the app
load_frame1()
root.mainloop()
