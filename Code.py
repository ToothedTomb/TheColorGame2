import tkinter
from tkinter import *
from tkinter import CENTER, ttk, messagebox
import tkinter.messagebox
import random
import os
from tkinter.ttk import *
import tkinter as tk
import sys
import sqlite3
colours = ['Red', 'Blue', 'Green', 'Pink', 'Black',
           'Yellow', 'Orange', 'White', 'Purple', 'Brown', 'Grey']
global score
score = 0
current_level = 1
global timeset
timeset = 50
global timeleft
timeleft = timeset
global level
level = 1  # New variable to track the level

conn = sqlite3.connect('Scores.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS highscores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER,
        level INTEGER
    )
''')
conn.commit()


# Functions will set up the levels
def level1():
    global current_level
    stop_countdown()
    current_level = 1
    global level, timeset, timeleft, score
    level = 1
    timeset = 100
    timeleft = timeset
    score = 0
    stop_countdown()
    timeLabel.config(text="Time left: " + str(timeleft))
    label.config(fg=root.cget("bg"), text="")
def level2():
    global current_level
    stop_countdown()
    current_level = 2
    global level, timeset, timeleft, score
    level = 2
    timeset = 50
    timeleft = timeset
    score = 0
    startGame(None)
    stop_countdown()
    timeLabel.config(text="Time left: " + str(timeleft))
    label.config(fg=root.cget("bg"), text="")
def level3():
    global current_level
    stop_countdown()
    current_level = 3
    global level, timeset, timeleft, score
    level = 3
    timeset = 30
    timeleft = timeset
    score = 0
    startGame(None)
    stop_countdown()
    timeLabel.config(text="Time left: " + str(timeleft))
    label.config(fg=root.cget("bg"), text="")
countdown_id = None  # Global variable to store the countdown ID

def stop_countdown():
    global countdown_id
    if countdown_id is not None:
        timeLabel.after_cancel(countdown_id)
        countdown_id = None

def startGame(event):
    global timeleft, countdown_id
    
    if level > 0:  # Check if a level is selected
        if timeleft == timeset:
            stop_countdown()  # Stop any ongoing countdown
            countdown_id = timeLabel.after(1000, countdown)  # Start a new countdown
        nextColour()

def save_score():
    global score, level
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO highscores (score, level) VALUES (?, ?)', (score, level))
    conn.commit()


def show_high_scores():
    cursor = conn.cursor()
    cursor.execute('''
        SELECT score, level FROM highscores
        ORDER BY score DESC LIMIT 10
    ''')
    highscores = cursor.fetchall()
    highscore_str = "High Scores:\n"
    for i, (score, level) in enumerate(highscores, start=1):
        highscore_str += f"{i}. Score: {score}, Level: {level}\n"
    tkinter.messagebox.showinfo("High Scores", highscore_str)


def nextColour():
    global score
    global timeleft
    global level

    if timeleft > 0 and level == current_level:
        e.focus_set()

        if e.get().lower() == colours[1].lower():
            score += 1
        else:
            score -= 1
            if score < 0:
                score = 0

        e.delete(0, tkinter.END)

        random.shuffle(colours)

        label.config(fg=str(colours[1]), text=str(colours[0]))

        scoreLabel.config(text="Points: " + str(score))
    if (timeleft == 0):
        save_score()



def countdown():
    global timeleft, level, countdown_id

    if timeleft > 0:
        timeleft -= 1
        timeLabel.config(text="Time left: " + str(timeleft))
        countdown_id = timeLabel.after(1000, countdown)
    elif level >= 3:  # Check if a level is selected
        stop_countdown()  # Stop the countdown when time runs out
        level += 1  # Increment to the next level
        if level <= 3:
            timeset = [100, 50, 20][level - 1]
            timeleft = timeset
            timeLabel.config(text="Time left: " + str(timeleft))
        nextColour()



root = tk.Tk()
root.title("The Color Game 2 - BETA!")
my_menu = Menu(root)
root.config(menu=my_menu)


def KeyboardShortcuts():
    root = tk.Toplevel()
    root.resizable(0, 0)
    root.attributes("-topmost", True)
    root.title("Keyboard Shortcuts.")

    labelTitle = ttk.Label(
        root, font=("Montserrat", 26, "bold", "underline"), anchor='center', text="Keyboard shortcuts.")
    label = ttk.Label(
        root, font=("Montserrat", 16, "bold",), anchor='center', text="Press the 'Escape key' to exit the game.")
    labelTitle.pack(side="top", fill="x", pady=1)
    label.pack(side="top", fill="x", pady=2)
    B1 = tk.Button(
        root, text="Exit", font=("Montserrat", 28), bg="pink", activebackground='#23d18b', command=root.destroy)
    B1.pack()


def whoMadeThisGame():
    root = tk.Toplevel()
    root.attributes("-topmost", True)
    root.resizable(0, 0)
    root.title("Who made this game?")
    root.tk.call('wm', 'iconphoto', root._w,
                 tkinter.PhotoImage(file='ColorGameForLinux.png'))

    labelTitle = ttk.Label(
        root, font=("Montserrat", 26, "bold", "underline"), anchor='center', text="Who made this game?")
    label = ttk.Label(
        root, font=("Montserrat", 16, "bold",), anchor='center', text="Jonathan Steadman has made this game.")
    labelTitle.pack(side="top", fill="x", pady=1)
    label.pack(side="top", fill="x", pady=2)
    B1 = tk.Button(
        root, text="Exit", font=("Montserrat", 28), bg="pink", activebackground='#23d18b', command=root.destroy)
    B1.pack()


def howtoplay():
    root = tk.Toplevel()
    root.attributes("-topmost", True)
    root.resizable(0, 0)
    root.title("How to play this game?")
    root.tk.call('wm', 'iconphoto', root._w,
                 tkinter.PhotoImage(file='ColorGameForLinux.png'))

    labelTitle = ttk.Label(
        root, font=("Montserrat", 26, "bold", "underline"), anchor='center', text="How to play this game?")
    label = ttk.Label(
        root, font=("Montserrat", 16, "bold",), anchor='center', text="You will need to type down the color of the text. Not what the text says what the color is.")
    label3 = ttk.Label(
        root, font=("Montserrat", 16, "bold",), anchor='center', text="You will need to be fast to get more points but needs to be written correctly and the right color.")
    labelw = ttk.Label(
        root, font=("Montserrat", 16, "bold",), anchor='center', text="You will lose one point if you make a mistake.")
    labelLevels = ttk.Label(
        root, font=("Montserrat", 16, "bold",), anchor='center', text="There are levels, the harder the level, the shorter time you have and you will need to be faster to type.")
    label4 = ttk.Label(
        root, font=("Montserrat", 16, "bold",), anchor='center', text="Press the enter key to submit your answer.")
    labelTitle.pack(side="top", fill="x", pady=1)
    label.pack(side="top", fill="x", pady=2)
    label3.pack(side="top", fill="x", pady=3)
    labelw.pack(side="top", fill="x", pady=4)
    labelLevels.pack(side="top",fill="x",pady=5)
    label4.pack(side="top", fill="x", pady=6)

    B1 = tk.Button(
        root, text="Exit", font=("Montserrat", 28), bg="pink", activebackground='#23d18b', command=root.destroy)
    B1.pack()


file_menu = Menu(my_menu, background="pink", activebackground="#23d18b")
my_menu.add_cascade(
    label="About:", font=("Montserrat", 18), activebackground="#23d18b", menu=file_menu)
file_menu.add_command(
    label="How to play this game?", font=("Montserrat", 18), activebackground="#23d18b", background="pink", command=howtoplay)
file_menu.add_command(
    label="Who made this game?", font=("Montserrat", 18), activebackground="#23d18b", background="pink", command=whoMadeThisGame)
file_menu.add_command(
    label="High Scores", font=("Montserrat", 18), activebackground="#23d18b", background="pink", command=show_high_scores)
file_menu.add_command(
    label="Keyboard shortcuts.", font=("Montserrat", 18), activebackground="#23d18b", background="pink", command=KeyboardShortcuts)

LevelMenu = Menu(my_menu, background="pink", activebackground="#23d18b")
my_menu.add_cascade(
    label="Levels:", font=("Montserrat", 18), activebackground="#23d18b", menu=LevelMenu)
LevelMenu.add_command(
    label="Easy - 100s.", font=("Montserrat", 18), activebackground="#23d18b", background="pink", command=level1)
LevelMenu.add_command(
    label="Medium - 50s.", font=("Montserrat", 18), activebackground="#23d18b", background="pink", command=level2)
LevelMenu.add_command(
    label="Hard - 30s.", font=("Montserrat", 18), activebackground="#23d18b", background="pink", command=level3)
my_menu.configure(bg="pink")
icon_image = tk.PhotoImage(file='ColorGameForLinux.png')
root.iconphoto(True, icon_image)

root.resizable(0, 0)

style = Style()
Help = tkinter.Label(root, text="The Color Game 2!",
                     font=('Montserrat', 24, "bold", "underline"))
Help.pack()
timeLabel = tkinter.Label(root, text="Time left " +
                          str(timeleft), font=('Montserrat', 28))
timeLabel.pack()
scoreLabel = tkinter.Label(root, text="Press enter to start:",
                           font=('Montserrat', 28))
scoreLabel.pack()
label = tkinter.Label(root, font=('Montserrat', 170))
label.pack()
e = tkinter.Entry(root, font=("Montserrat", 28), bg='#23d18b',border='7px')
root.bind('<Return>', startGame)
e.pack()

e.focus_set()
def KeyPressEsc(event):
    root = tk.Toplevel()
    root.attributes("-topmost", True)
    root.resizable(0, 0)
    root.title("Confirm to exit the game:")
    root.tk.call('wm', 'iconphoto', root._w,
                 tkinter.PhotoImage(file='ColorGameForLinux.png'))

    labelTitle = ttk.Label(
        root, font=("Montserrat", 26, "bold", "underline"), anchor='center', text="Confirm to exit the game:")
    label = ttk.Label(
        root, font=("Montserrat", 16, "bold",), anchor='center', text="Are you sure you want to leave this game?")

    labelTitle.pack(side="top", fill="x", pady=1)
    label.pack(side="top", fill="x", pady=2)
    B1 = tk.Button(
        root, text="Yes", font=("Montserrat", 28), bg="pink", activebackground='#23d18b', command=root.quit)

    B2 = tk.Button(
        root, text="No", font=("Montserrat", 28), bg="pink", activebackground='#23d18b', command=root.destroy)
    B1.pack(side=tkinter.LEFT, anchor=CENTER)
    B2.pack(side=tkinter.RIGHT, anchor=CENTER)


def on_closing():
    root = tk.Toplevel()
    root.attributes("-topmost", True)
    root.resizable(0, 0)
    root.title("Confirm to exit the game:")
    root.tk.call('wm', 'iconphoto', root._w,
                 tkinter.PhotoImage(file='ColorGameForLinux.png'))

    labelTitle = ttk.Label(
        root, font=("Montserrat", 26, "bold", "underline"), anchor='center', text="Confirm to exit the game:")
    label = ttk.Label(
        root, font=("Montserrat", 16, "bold",), anchor='center', text="Are you sure you want to leave this game?")

    labelTitle.pack(side="top", fill="x", pady=1)
    label.pack(side="top", fill="x", pady=2)
    B1 = tk.Button(
        root, text="Yes", font=("Montserrat", 28), bg="pink", activebackground='#23d18b', command=root.quit)

    B2 = tk.Button(
        root, text="No", font=("Montserrat", 28), bg="pink", activebackground='#23d18b', command=root.destroy)
    B1.pack(side=tkinter.LEFT, anchor=CENTER)
    B2.pack(side=tkinter.RIGHT, anchor=CENTER)


root.geometry("900x500")

root.bind('<Escape>', KeyPressEsc)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()